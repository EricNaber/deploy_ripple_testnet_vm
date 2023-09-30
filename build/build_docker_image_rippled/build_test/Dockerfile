FROM ubuntu:latest

RUN export LANGUAGE=C.UTF-8; export LANG=C.UTF-8; export LC_ALL=C.UTF-8; export DEBIAN_FRONTEND=noninteractive

COPY entrypoint /entrypoint.sh
COPY install ./install.sh

# Setup C++ development environment (with git, python, conan, cmake, gcc
RUN apt-get update -y && apt-get install git -y
RUN /bin/bash -c "chmod +x ./install.sh"
RUN /bin/bash -c "./install.sh"

# Set up conan
RUN /bin/bash -c "conan profile new default --detect"
RUN /bin/bash -c "conan profile update settings.compiler.cppstd=20 default"

# Build and Test rippled
RUN /bin/bash -c "mkdir .build"
RUN /bin/bash -c "cd .build"
#RUN /bin/bash -c "conan install .. --output-folder . --build missing --setting build_type=Release"
#RUN /bin/bash -c "conan install .. --output-folder . --build missing --settings build_type=Release --settings compiler.runtime=MT"
RUN /bin/bash -c "cmake -DCMAKE_TOOLCHAIN_FILE:FILEPATH=build/generators/conan_toolchain.cmake -DCMAKE_BUILD_TYPE=Release .."
RUN /bin/bash -c "cmake --build ."

