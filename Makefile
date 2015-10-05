CFLAGS = -m64 -O3 -flto -funroll-loops -DNDEBUG -Wall -Wextra -ansi -pedantic -I/home/joao/Software/DNest3/include -I/home/joao/Software/RJObject
LIBS = -lrjobject -ldnest3 -lgsl -lgslcblas -lboost_thread -lboost_system -L/home/joao/Software/RJObject -L/home/joao/Software/DNest3/lib

default:
	g++ $(CFLAGS) -c *.cpp
	g++ -o main *.o $(LIBS)
	rm -f *.o

