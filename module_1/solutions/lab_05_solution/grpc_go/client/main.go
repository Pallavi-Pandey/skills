// Lab 05 - gRPC Client (SOLUTION)
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

	"lab05grpc/calculator"
)

func main() {
	serverAddr := flag.String("server", "localhost:50051", "gRPC server address")
	flag.Parse()

	conn, err := grpc.Dial(*serverAddr, grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	defer conn.Close()

	client := calculator.NewCalculatorClient(conn)

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	fmt.Println("=== gRPC Calculator Client ===")
	fmt.Println()

	ops := []struct {
		op   string
		a, b float64
	}{
		{"add", 42, 18},
		{"subtract", 42, 18},
		{"multiply", 42, 18},
		{"divide", 42, 0},
	}
	for _, o := range ops {
		resp, err := client.Calculate(ctx, &calculator.CalcRequest{
			Operation: o.op,
			A:         o.a,
			B:         o.b,
		})
		if err != nil {
			log.Fatalf("Calculate failed: %v", err)
		}
		if resp.Error != "" {
			fmt.Printf("%s(%.0f, %.0f) -> ERROR: %s\n", o.op, o.a, o.b, resp.Error)
		} else {
			fmt.Printf("%s(%.0f, %.0f) -> %.0f\n", o.op, o.a, o.b, resp.Result)
		}
	}

	fmt.Println()
	fmt.Println("Fibonacci stream:")
	stream, err := client.FibonacciStream(ctx, &calculator.FibRequest{Count: 10})
	if err != nil {
		log.Fatalf("FibonacciStream failed: %v", err)
	}
	for {
		resp, err := stream.Recv()
		if err == io.EOF {
			break
		}
		if err != nil {
			log.Fatalf("stream error: %v", err)
		}
		fmt.Printf("  Fibonacci[%d] = %d\n", resp.Index, resp.Value)
	}
}
