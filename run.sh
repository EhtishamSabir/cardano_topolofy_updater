export LD_LIBRARY_PATH="/usr/local/lib:$LD_LIBRARY_PATH"
export PKG_CONFIG_PATH="/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH"
export CARDANO_NODE_SOCKET_PATH=/home/ehtishaamupwork/relay/db/node.socket

/home/ehtishaamupwork/.local/bin/cardano-node run \
   --topology /home/ehtishaamupwork/relay/mainnet-topology.json \
   --database-path /home/ehtishaamupwork/relay/db \
   --socket-path /home/ehtishaamupwork/relay/db/node.socket \
   --host-addr 0.0.0.0 \
   --port 3001 \
   --config /home/ehtishaamupwork/relay/mainnet-config.json

