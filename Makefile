#CC = gcc
CC = g++
TARGET = test

all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(CC)  *.cpp -ggdb3 -pg -lm -o  $@
