import algosdk, { getApplicationAddress } from "algosdk";
import {
  getLocalAccounts,
  getLocalAlgodClient,
  getLocalIndexerClient,
  getMainnetAlgodClient,
  getMainnetIndexerClient,
  getTestnetAlgodClient,
  getTestnetAlgodClientTUM,
  printCurrentRound,
  printMempoolTransactions,
  SandboxAccount,
} from "./utils";
import fs from "fs";
import path from "path";
import { plotBasedOnFee } from "./plots";

async function sendTransaction(
  algodClient: algosdk.Algodv2,
  privateKey: Uint8Array,
  receiverAddress: string,
  amount: number
): Promise<string> {
  // const algodClient = getMainnetAlgodClient();
  console.log(`algodClient: ${algodClient}`);
  const senderAddress = algosdk.encodeAddress(privateKey.slice(32));
  console.log(`Sender address: ${senderAddress}`);

  console.log("Account:  ", receiverAddress);

  console.log(
    `Sending ${
      amount / 1000000
    } Algos from ${senderAddress} to ${receiverAddress}`
  );
  const params = await algodClient.getTransactionParams().do();
  const note = Buffer.from("Hello Algorand!");
  const noteUint8Array = new Uint8Array(
    note.buffer,
    note.byteOffset,
    note.byteLength
  );
  console.log("Default Params: ", params);
  const transaction = {
    from: senderAddress,
    to: receiverAddress,
    fee: 1000,
    amount: amount,
    firstRound: params.firstRound,
    lastRound: params.lastRound,
    genesisID: params.genesisID,
    genesisHash: params.genesisHash,
    note: noteUint8Array,
  };

  const signedTransaction = algosdk.signTransaction(transaction, privateKey);
  const txId = signedTransaction.txID;
  try {
    const status = await algodClient.status().do();
    console.log("Current round:", status["last-round"]);
  } catch (error) {
    console.error("Error getting the current round:", error);
  }

  await algodClient.sendRawTransaction(signedTransaction.blob).do();
  return txId;
}

async function callMethod(
  myAccount: any,
  algodClient: algosdk.Algodv2,
  algodClientTUM: algosdk.Algodv2
): Promise<void> {
  // Define the application id of the smart contract
  // Get the suggested parameters from the Algorand node
  let params = await algodClient.getTransactionParams().do();
  let params2 = await algodClientTUM.getTransactionParams().do();

  const appId = 221739623;
  const atc1 = new algosdk.AtomicTransactionComposer();
  const atc2 = new algosdk.AtomicTransactionComposer();
  const abi = JSON.parse(
    fs.readFileSync(path.join(__dirname, "/application.json"), "utf8")
  );
  // const signer = new algosdk.Account(myAccount.sk);

  const contract = new algosdk.ABIContract(abi.contract);
  const appInfo = await algodClient.getApplicationByID(appId).do();
  console.log("Previous state: ", appInfo["params"]["global-state"]);

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
    suggestedParams: params,
  });

  // (async () => {
  //   let latestBlockNumber = (await algodClient.status().do()).lastRound;
  //   let blockInfo = await algodClient.block(latestBlockNumber).do();
  //   console.log(blockInfo);
  // })();

  // printCurrentRound(algodClient);
  const CurrentAppInfo = await algodClient.getApplicationByID(appId).do();
  const previous_state = CurrentAppInfo["params"]["global-state"][0].value.uint;
  console.log("Previous state: ", previous_state);
  // printMempoolTransactions(algodClient);
  const retVal = await Promise.all([
    atc1.submit(algodClient),
    atc2.submit(algodClient),
  ]);
  // printMempoolTransactions(algodClient);
  // printMempoolTransactions(algodClientTUM);
  // printCurrentRound(algodClient);
  // printCurrentRound(algodClientTUM);

  await waitForConfirmation(algodClient, retVal[0][0]);
  await waitForConfirmation(algodClient, retVal[1][0]);

  console.log("Result 1: ", retVal[0][0]);
  console.log("Result 2: ", retVal[1][0]);

  const updatedAppInfo = await algodClient.getApplicationByID(appId).do();
  const updated_state = updatedAppInfo["params"]["global-state"][0].value.uint;
  console.log("Updated state: ", updated_state);
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
}

async function main() {
  const algodClient: algosdk.Algodv2 = getTestnetAlgodClient();
  const algodClientTUM: algosdk.Algodv2 = getTestnetAlgodClientTUM();
  // const indexerClient: algosdk.Indexer = getMainnetIndexerClient();
  const privateKey = algosdk.mnemonicToSecretKey(
    process.env.MNEMONIC as string
  );

  // console.log(`Private key: ${Buffer.from(privateKey.sk).toString("base64")}`);
  // const response: Record<string, any> = await getMemPoolTransactions(
  //   algodClient
  // );
  // console.log(response);
  // // console.log(response["top-transactions"]);

  // console.log("TXNS: ", algosdk.encodeAddress(response["top-transactions"][0]));

  // const accounts = await getLocalAccounts();
  // const sender = accounts[0];
  // console.log(`Actual Sender address: ${sender.addr}`);
  const receiverAddress =
    "PPYFRUNMRJCS2WXDQTDTOEK22HJUYQ6DOSXZM3GTRKTVDADTRI6QWAW7DQ";
  const amount = 1_000; // microAlgos
  // const transactionSearch = await indexerClient
  //   .searchForTransactions()
  //   .txid("2H65N44WGVLF2DVRHNMNS7Y2EKKBZ3XNWCB5W6TJMLWZUNOJRMTA")
  //   .do();
  // console.log(transactionSearch);
  // console.log(`isvalid address: ${algosdk.isValidAddress(receiverAddress)}`);
  try {
    // const txId = await sendTransaction(
    //   algodClient,
    //   privateKey.sk,
    //   receiverAddress,
    //   amount
    // );
    // console.log(`Transaction sent! Transaction ID: ${txId}`);
    // await callMethod(privateKey, algodClient, algodClientTUM);
    await plotBasedOnFee(privateKey, algodClient);
  } catch (error) {
    console.error(`Error sending transaction: ${error}`);
  }
}

main();
