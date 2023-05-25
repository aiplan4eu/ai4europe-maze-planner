# AIDDL/UP Executor

This version of the executor uses the full unified planning service.

## Compile Protobuf to Python Code

    python3 -m grpc_tools.protoc --python_out=. --proto_path=. --grpc_python_out=. *.proto
