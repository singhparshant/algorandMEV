package main

import (
	"context"
	"fmt"
	"os"
	"time"

	"github.com/algorand/go-algorand-sdk/client/v2/indexer"
)

var prevCounter uint64 = 465260475 // 30679587 - 1153474356, 30707921 - 1154159924, 17742590 - 448718363

func getTUMIndexerClient() (*indexer.Client, error) {
	indexerServer := "https://mainnet-idx.algonode.network" //"http://131.159.14.109:8981"
	indexerToken := "ODBHPZFSZLRGDZMJDMLR8B24GUKLFXAY"      //os.Getenv("TOKEN_TUM_MAINNET")
	client, err := indexer.MakeClient(indexerServer, indexerToken)
	return client, err
}

func main() {
	// Initialize Algorand SDK
	indexerClient, err := getTUMIndexerClient() // Assume this function is defined
	if err != nil {
		panic("Failed to create algod client: " + err.Error())
	}

	// Create a map to store the results
	resultMap := make(map[uint64]uint64)

	// Assign work to the worker pool
	for round := uint64(18002592); round <= 18702591; round++ {
		time.Sleep(20 * time.Millisecond) // sleep for 25 ms
		block := indexerClient.LookupBlock(round)
		block.HeaderOnly(true)
		res, err := block.Do(context.Background())
		// fmt.Println("Txns count: ", res.TxnCounter)
		numTxns := uint64(res.TxnCounter - prevCounter)
		prevCounter = res.TxnCounter

		if err != nil {
			fmt.Println("ERR: ", err)
		}

		if numTxns > uint64(300) {
			fmt.Println("Block ", round, " has ", numTxns, " transactions")
		}

		if numTxns > uint64(2000) {
			resultMap[round] = numTxns
		}
	}

	// Write the results to the file
	f, err := os.OpenFile("results.csv", os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		fmt.Println("Error opening file: ", err)
		return
	}
	defer f.Close()

	// Write the headers
	if _, err := f.WriteString("Block,Transactions\n"); err != nil {
		fmt.Println("Error writing to file: ", err)
	}

	fmt.Println("Writing results to file...", resultMap)

	// Write the data
	for round, numTxns := range resultMap {
		result := fmt.Sprintf("%d,%d\n", round, numTxns)
		if _, err := f.WriteString(result); err != nil {
			fmt.Println("Error writing to file: ", err)
		}
	}
}
