import algosdk from "algosdk";
import {
  getLocalAccounts,
  getLocalAlgodClient,
  getLocalIndexerClient,
  getMainnetAlgodClient,
  getMainnetIndexerClient,
  getMemPoolTransactions,
  SandboxAccount,
} from "./utils";

async function sendTransaction(
  privateKey: Uint8Array,
  receiverAddress: string,
  amount: number
): Promise<string> {
  const algodClient = getMainnetAlgodClient();
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
  console.log(
    "Mempool Before: ",
    (await getMemPoolTransactions(algodClient))["top-transactions"].map(
      (result: any) => algosdk.encodeAddress(result.txn.snd)
    )
  );
  await algodClient.sendRawTransaction(signedTransaction.blob).do();
  console.log(
    "Mempool After: ",
    (await getMemPoolTransactions(algodClient))["top-transactions"]
  );
  return txId;
}

async function main() {
  const algodClient: algosdk.Algodv2 = getMainnetAlgodClient();
  // const indexerClient: algosdk.Indexer = getMainnetIndexerClient();
  const privateKey = algosdk.mnemonicToSecretKey(
    process.env.MNEMONIC as string
  );
  console.log(`Private key: ${Buffer.from(privateKey.sk).toString("base64")}`);
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
    const txId = await sendTransaction(privateKey.sk, receiverAddress, amount);
    console.log(`Transaction sent! Transaction ID: ${txId}`);
  } catch (error) {
    console.error(`Error sending transaction: ${error}`);
  }
}

main();
