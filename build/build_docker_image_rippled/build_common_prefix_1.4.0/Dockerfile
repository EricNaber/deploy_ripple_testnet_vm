FROM ubuntu:18.04

# Install dependencies
RUN /bin/bash -c "apt update -y && apt upgrade -y"
RUN /bin/bash -c "apt install gcc g++ wget git cmake protobuf-compiler libprotobuf-dev libssl-dev -y"

# clone Github-Project
RUN /bin/bash -c "git clone https://github.com/EricNaber/rippled.git"
RUN /bin/bash -c "cd rippled && git checkout common_prefix_attack"

# Build Boost for compiling
RUN /bin/bash -c "wget https://boostorg.jfrog.io/artifactory/main/release/1.70.0/source/boost_1_70_0.tar.gz && \
                  tar -xzf boost_1_70_0.tar.gz && \
                  rm boost_1_70_0.tar.gz"
RUN /bin/bash -c "cd boost_1_70_0 && \
                  ./bootstrap.sh"
RUN /bin/bash -c "cd boost_1_70_0 && \
                  ./b2 headers"
RUN /bin/bash -c "cd boost_1_70_0 && \
                  ./b2"

# Compile Codebase
RUN /bin/bash -c "cd rippled && \
                  export BOOST_ROOT=/boost_1_70_0 && \
                  mkdir .build && \
                  cd .build && \
                  cmake -DCMAKE_BUILD_TYPE=Debug .."
RUN /bin/bash -c "cd rippled/.build && \
                  cmake --build ."

# Create ripple-config directory and add rippled to binary
RUN /bin/bash -c "mkdir /etc/opt/ripple/"
RUN /bin/bash -c "ln -s /rippled/.build/rippled /usr/local/sbin/"

# Execute rippled on startup
ENTRYPOINT [ "rippled" ]
