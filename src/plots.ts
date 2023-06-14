import algosdk from "algosdk";
import PendingTransactionInformation from "algosdk/dist/types/client/v2/algod/pendingTransactionInformation";
require("dotenv").config();
import fs from "fs";
import path from "path";
// import * as Plotly from "plotly.js";
const Plotly = require("plotly")("sipars", "XtWfvr3wQaNbH5CDwJdY");

export async function plotBasedOnFee(
  myAccount: any,
  algodClient: algosdk.Algodv2,
  algodClientTUM?: algosdk.Algodv2
): Promise<void> {
  // Define the application id of the smart contract
  // Get the suggested parameters from the Algorand node

  const appId = 224977223;
  const abi = JSON.parse(
    fs.readFileSync(path.join(__dirname, "/application.json"), "utf8")
  );
  let countsOfDecrement: number[] = [];
  let countsOfIncrement: number[] = [];

  const contract = new algosdk.ABIContract(abi.contract);
  let atc1, atc2, params;
  for (let i = 1; i <= 5; i++) {
    atc1 = new algosdk.AtomicTransactionComposer();
    atc2 = new algosdk.AtomicTransactionComposer();
    params = await algodClient.getTransactionParams().do();
    atc1.addMethodCall({
      appID: appId,
      method: contract.getMethodByName("decrement"),
      methodArgs: [],
      sender: myAccount.addr,
      signer: algosdk.makeBasicAccountTransactionSigner(myAccount),
      suggestedParams: params,
    });

    atc2.addMethodCall({
      appID: appId,
      method: contract.getMethodByName("increment"),
      methodArgs: [],
      sender: myAccount.addr,
      signer: algosdk.makeBasicAccountTransactionSigner(myAccount),
      suggestedParams: {
        ...params,
        fee: 500,
      },
    });
    const currentAppInfo = await algodClient.getApplicationByID(appId).do();
    const previous_state =
      currentAppInfo["params"]["global-state"][0].value.uint;
    console.log("Previous state: ", previous_state);
    // printMempoolTransactions(algodClient);
    const retVal = await Promise.all([
      atc1.submit(algodClient),
      atc2.submit(algodClient),
    ]);

    console.log("Result 1: ", retVal[0][0]);
    console.log("Result 2: ", retVal[1][0]);

    const atc1_confirmation = await waitForConfirmation(
      algodClient,
      retVal[0][0]
    );
    const atc2_confirmation = await waitForConfirmation(
      algodClient,
      retVal[1][0]
    );

    await Promise.all([
      waitForConfirmation(algodClient, retVal[0][0]),
      waitForConfirmation(algodClient, retVal[1][0]),
    ]);

    // Check if both transactions are confirmed in the same round
    // if (
    //   atc1_confirmation.confirmed_round === atc2_confirmation.confirmed_round
    // ) {
    //   const block_info = await algodClient
    //     .block(atc1_confirmation.confirmed_round)
    //     .do();
    //   const transactions = block_info.transactions;

    //   const atc1_index = transactions.findIndex(txn => txn.tx === atc1_txn_id);
    //   const atc2_index = transactions.findIndex(txn => txn.tx === atc2_txn_id);

    //   if (atc1_index < atc2_index) {
    //     console.log(
    //       "Transaction 1 (decrement) was executed before Transaction 2 (increment)."
    //     );
    //   } else if (atc1_index > atc2_index) {
    //     console.log(
    //       "Transaction 2 (increment) was executed before Transaction 1 (decrement)."
    //     );
    //   } else {
    //     console.log("Both transactions were executed in the same round.");
    //   }
    // } else {
    //   console.log("Transactions were not confirmed in the same round.");
    // }

    const updatedAppInfo = await algodClient.getApplicationByID(appId).do();
    const updated_state =
      updatedAppInfo["params"]["global-state"][0].value.uint;
    console.log("Updated state: ", updated_state);

    // if ((previous_state * 3) / 2 - 1 === updated_state) {
    //   countsOfIncrement.push(i);
    //   console.log("Incremented first.");
    // } else if (((previous_state - 1) * 3) / 2 === updated_state) {
    //   countsOfDecrement.push(i);
    //   console.log("Decremented first.");
    // } else {
    //   console.log("Somethin  g went wrong");
    //   break;
    // }
  }
  // barGraphplot(countsOfDecrement, countsOfIncrement);
  scatterGraphPlot(countsOfDecrement, countsOfIncrement);
}

async function waitForConfirmation(algodClient: algosdk.Algodv2, txId: string) {
  let confirmedRound = null;
  while (confirmedRound === null) {
    const pendingInfo = await algodClient
      .pendingTransactionInformation(txId)
      .do();
    if (pendingInfo["confirmed-round"]) {
      confirmedRound = pendingInfo["confirmed-round"];
    } else {
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  }
  console.log("Transaction confirmed in round", confirmedRound);
  const block_info = await algodClient.block(confirmedRound).do();
  console.log("Block info: %o", block_info);
}

async function barGraphplot(
  countsOfDecrement: number[],
  countsOfIncrement: number[]
) {
  let traceA = {
    x: countsOfDecrement,
    y: new Array(countsOfDecrement.length).fill(1),
    name: "Decrement",
    type: "bar" as const,
  };

  let traceB = {
    x: countsOfIncrement,
    y: new Array(countsOfIncrement.length).fill(1),
    name: "Increment",
    type: "bar" as const,
  };

  let data = [traceA, traceB];

  let layout: Partial<Plotly.Layout> = {
    barmode: "stack",
    title: "Function Execution Order",
    xaxis: { title: "Iteration" },
    yaxis: { title: "Count" },
  };

  // Plotly.plot("myDiv", data, layout);
  // Plotly.plot(data, config, function (err, msg) {
  //   console.log(msg);
  // });
}

async function scatterGraphPlot(
  countsOfDecrement: number[],
  countsOfIncrement: number[]
) {
  let traceA: Partial<Plotly.ScatterData> = {
    x: countsOfDecrement,
    y: new Array(countsOfDecrement.length).fill("Decrement"),
    mode: "markers",
    type: "scatter",
    name: "Decrement",
    marker: { color: "blue" },
  };

  let traceB: Partial<Plotly.ScatterData> = {
    x: countsOfIncrement,
    y: new Array(countsOfIncrement.length).fill("Increment"),
    mode: "markers",
    type: "scatter",
    name: "Increment",
    marker: { color: "red" },
  };

  let data = [traceA, traceB];

  let layout = {
    title: "Function Execution Order",
    xaxis: { title: "Iteration" },
    yaxis: { title: "Function Executed" },
  };

  let config = {
    responsive: true,
  };

  // console.log("data: ", data);

  // Plotly.plot(data, layout, config);
  var graphOptions = {
    layout: layout,
    filename: "line-style",
    fileopt: "overwrite",
  };
  Plotly.plot(data, graphOptions, function (err, msg) {
    console.log(msg);
  });
}
