FROM ubuntu:latest

COPY ./install /install.sh
COPY ./transaction1 /transaction1.sh
COPY ./transaction_dest1 /transaction_dest1.sh
COPY ./transaction_dest2 /transaction_dest2.sh

# Setup C++ development environment (with git, python, conan, cmake and a cpp-compiler)
RUN /bin/bash -c "apt update -y && apt upgrade -y"
RUN /bin/bash -c "apt install git unzip wget -y"
RUN /bin/bash -c "chmod +x /install.sh"
RUN /bin/bash -c "/install.sh"
RUN /bin/bash -c "rm /install.sh"

# Clone rippled from github
# RUN /bin/bash -c "git clone https://github.com/XRPLF/rippled.git"
RUN /bin/bash -c "wget https://github.com/XRPLF/rippled/archive/refs/tags/1.12.0.zip"
RUN /bin/bash -c "unzip 1.12.0.zip"
RUN /bin/bash -c "mv rippled-1.12.0 rippled"

# Setup conan profile
RUN /bin/bash -c "conan profile new default --detect"
RUN /bin/bash -c "conan profile update settings.compiler.cppstd=20 default"
RUN /bin/bash -c "conan profile update settings.compiler.libcxx=libstdc++11 default"

# Build
RUN /bin/bash -c "mkdir /rippled/.build"
RUN /bin/bash -c "conan install /rippled/ --output-folder /rippled/.build/ --build missing --settings build_type=Release"
RUN /bin/bash -c "cd /rippled/.build/ && \
                  cmake -DCMAKE_TOOLCHAIN_FILE:FILEPATH=build/generators/conan_toolchain.cmake -DCMAKE_BUILD_TYPE=Release .."
RUN /bin/bash -c "cmake --build /rippled/.build/ --config Release"
RUN /bin/bash -c "mkdir /etc/opt/ripple/"
RUN /bin/bash -c "ln -s /rippled/.build/rippled /usr/local/sbin/"

# make transactions executable
RUN /bin/bash -c "chmod +x /transaction1.sh"
RUN /bin/bash -c "chmod +x /transaction_dest1.sh"
RUN /bin/bash -c "chmod +x /transaction_dest2.sh"

ENTRYPOINT [ "rippled" ]
