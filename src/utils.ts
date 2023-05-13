import algosdk from "algosdk";
require("dotenv").config();

export interface SandboxAccount {
  addr: string;
  privateKey: Uint8Array;
  signer: algosdk.TransactionSigner;
}

export async function getLocalAccounts(): Promise<SandboxAccount[]> {
  const kmdClient = getLocalKmdClient();

  const wallets = await kmdClient.listWallets();

  let walletId;
  // eslint-disable-next-line no-restricted-syntax
  for (const wallet of wallets.wallets) {
    if (wallet.name === "unencrypted-default-wallet") walletId = wallet.id;
  }

  if (walletId === undefined)
    throw Error("No wallet named: unencrypted-default-wallet");

  const handleResp = await kmdClient.initWalletHandle(walletId, "");
  const handle = handleResp.wallet_handle_token;

  const addresses = await kmdClient.listKeys(handle);
  // eslint-disable-next-line camelcase
  const acctPromises: Promise<{ private_key: Buffer }>[] = [];

  // eslint-disable-next-line no-restricted-syntax
  for (const addr of addresses.addresses) {
    acctPromises.push(kmdClient.exportKey(handle, "", addr));
  }
  const keys = await Promise.all(acctPromises);

  // Don't need to wait for it
  kmdClient.releaseWalletHandle(handle);

  return keys.map(k => {
    const addr = algosdk.encodeAddress(k.private_key.slice(32));
    const acct = { sk: k.private_key, addr } as algosdk.Account;
    const signer = algosdk.makeBasicAccountTransactionSigner(acct);

    return {
      addr: acct.addr,
      privateKey: acct.sk,
      signer,
    };
  });
}

export function getLocalKmdClient() {
  const kmdToken = "a".repeat(64);
  const kmdServer = "http://localhost";
  const kmdPort = process.env.KMD_PORT || "4002";

  const kmdClient = new algosdk.Kmd(kmdToken, kmdServer, kmdPort);
  return kmdClient;
}

export function getLocalIndexerClient() {
  const indexerToken = "a".repeat(64);
  const indexerServer = "http://localhost";
  const indexerPort = process.env.INDEXER_PORT || "8980";

  const indexerClient = new algosdk.Indexer(
    indexerToken,
    indexerServer,
    indexerPort
  );
  return indexerClient;
}

export function getLocalAlgodClient() {
  const algodToken = "a".repeat(64);
  const algodServer = "http://localhost";
  const algodPort = process.env.ALGOD_PORT || "4001";

  const algodClient = new algosdk.Algodv2(algodToken, algodServer, algodPort);
  return algodClient;
}

export function getMainnetAlgodClient(): algosdk.Algodv2 {
  const algodToken: any = {
    "X-API-key": process.env.TOKEN,
  };
  const algodServer = "https://testnet-algorand.api.purestake.io/ps2";
  const algodPort = process.env.ALGOD_PORT || "";
  const algodClient = new algosdk.Algodv2(algodToken, algodServer, algodPort);
  return algodClient;
}

export function getMainnetIndexerClient(): algosdk.Indexer {
  const algodToken: any = {
    "X-API-key": process.env.TOKEN,
  };
  const indexerServer = "https://testnet-algorand.api.purestake.io/idx2";
  const indexerPort = process.env.INDEXER_PORT || "";
  const indexerClient = new algosdk.Indexer(
    algodToken,
    indexerServer,
    indexerPort
  );
  return indexerClient;
}

export async function getMemPoolTransactions(
  algodClient: algosdk.Algodv2
): Promise<Record<string, any>> {
  const pendingTxns: Record<string, any> = await algodClient
    .pendingTransactionsInformation()
    .max(10)
    .do();
  return pendingTxns;
}
