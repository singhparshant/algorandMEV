import algosdk from "algosdk";
import {
  getLocalAccounts,
  getLocalAlgodClient,
  getLocalIndexerClient,
  SandboxAccount,
} from "./utils";

async function sendTransaction(
  privateKey: Uint8Array,
  receiverAddress: string,
  amount: number
): Promise<string> {
  const algodClient = getLocalAlgodClient();

  const senderAddress = algosdk.encodeAddress(privateKey.slice(32));
  console.log(`Sender address: ${senderAddress}`);

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

  const transaction = {
    from: senderAddress,
    to: receiverAddress,
    fee: params.fee,
    amount: amount,
    firstRound: params.firstRound,
    lastRound: params.lastRound,
    genesisID: params.genesisID,
    genesisHash: params.genesisHash,
    note: noteUint8Array,
  };

  const signedTransaction = algosdk.signTransaction(transaction, privateKey);
  const txId = signedTransaction.txID;
  await algodClient.sendRawTransaction(signedTransaction.blob).do();

  return txId;
}

async function main() {
  const accounts = await getLocalAccounts();
  const sender = accounts[0];
  console.log(`Actual Sender address: ${sender.addr}`);

  const receiverAddress =
    "A7NMWS3NT3IUDMLVO26ULGXGIIOUQ3ND2TXSER6EBGRZNOBOUIQXHIBGDE";
  const amount = 1_000_000; // 1 Algo
  console.log(`isvalid address: ${algosdk.isValidAddress(receiverAddress)}`);
  try {
    const txId = await sendTransaction(
      sender.privateKey,
      receiverAddress,
      amount
    );
    console.log(`Transaction sent! Transaction ID: ${txId}`);
  } catch (error) {
    console.error(`Error sending transaction: ${error}`);
  }
}

main();
