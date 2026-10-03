// Lab 05 - gRPC Server (Starter Code)
// =====================================
// Implements the Calculator gRPC service.
//
// Fill in the TODOs.

package main

import (
	"fmt"
	"log"
	"net"

	"google.golang.org/grpc"
	// TODO: Import your generated calculator package
	// Hint: After running protoc (see the lab README), import "lab05grpc/calculator"
)

const port = ":50051"

// server implements the Calculator service
type server struct {
	// TODO: Embed the generated UnimplementedCalculatorServer
}

// Calculate handles a unary RPC: performs arithmetic on two numbers
// TODO: Implement this method
// func (s *server) Calculate(ctx context.Context, req *calculator.CalcRequest) (*calculator.CalcResponse, error) {
//     switch req.Operation {
//     case "add":
//         return &calculator.CalcResponse{Result: req.A + req.B}, nil
//     case "subtract":
//         return &calculator.CalcResponse{Result: req.A - req.B}, nil
//     case "multiply":
//         return &calculator.CalcResponse{Result: req.A * req.B}, nil
//     case "divide":
//         if req.B == 0 {
//             return &calculator.CalcResponse{Error: "division by zero"}, nil
//         }
//         return &calculator.CalcResponse{Result: req.A / req.B}, nil
//     default:
//         return &calculator.CalcResponse{Error: "unknown operation"}, nil
//     }
// }

// FibonacciStream handles a server-streaming RPC: sends Fibonacci numbers one by one
// TODO: Implement this method
// func (s *server) FibonacciStream(req *calculator.FibRequest, stream calculator.Calculator_FibonacciStreamServer) error {
//     a, b := int64(0), int64(1)
//     for i := int32(0); i < req.Count; i++ {
//         stream.Send(&calculator.FibResponse{Value: a, Index: i})
//         a, b = b, a+b
//     }
//     return nil
// }

func main() {
	lis, err := net.Listen("tcp", port)
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}

	s := grpc.NewServer()
	// TODO: Register your server implementation
	// calculator.RegisterCalculatorServer(s, &server{})

	fmt.Printf("gRPC Calculator Server listening on %s\n", port)
	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
