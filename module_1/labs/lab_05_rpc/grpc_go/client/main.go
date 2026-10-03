// Lab 05 - gRPC Client (Starter Code)
// =====================================
// Calls the Calculator gRPC service.
//
// Fill in the TODOs.

package main

import (
	"context"
	"flag"
	"fmt"
	"io"
	"log"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	// TODO: Import your generated calculator package
	// Hint: After running protoc (see the lab README), import "lab05grpc/calculator"
)

func main() {
	serverAddr := flag.String("server", "localhost:50051", "gRPC server address")
	flag.Parse()

	// TODO: Dial the gRPC server
	// conn, err := grpc.Dial(*serverAddr, grpc.WithTransportCredentials(insecure.NewCredentials()))
	// if err != nil { log.Fatalf(...) }
	// defer conn.Close()

	// TODO: Create a Calculator client
	// client := calculator.NewCalculatorClient(conn)

	// TODO: Set a timeout context
	// ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	// defer cancel()

	fmt.Println("=== gRPC Calculator Client ===\n")

	// TODO: Call Calculate with different operations
	// Example:
	// resp, err := client.Calculate(ctx, &calculator.CalcRequest{
	//     Operation: "add",
	//     A: 42,
	//     B: 18,
	// })
	// fmt.Printf("42 + 18 = %.0f\n", resp.Result)

	// TODO: Call FibonacciStream to get streaming results
	// stream, err := client.FibonacciStream(ctx, &calculator.FibRequest{Count: 10})
	// for {
	//     resp, err := stream.Recv()
	//     if err == io.EOF { break }
	//     fmt.Printf("  Fibonacci[%d] = %d\n", resp.Index, resp.Value)
	// }

	// Suppress unused import/variable warnings during development —
	// remove these once you've filled in the TODOs above and actually use them.
	_ = context.Background
	_ = io.EOF
	_ = time.Second
	_ = insecure.NewCredentials
	_ = grpc.WithTransportCredentials
	_ = log.Fatalf
	_ = serverAddr
}
