includes = -I/usr/include/eigen3 -I/home/joao/Software/DNest3/include -I/home/joao/Software/RJObject
link = -L/home/joao/Software/RJObject -L/home/joao/Software/DNest3/lib

CFLAGS = -m64 -O3 -flto -funroll-loops -DNDEBUG -Wall -Wextra -ansi $(includes)
LIBS = -lrjobject -ldnest3 -lgsl -lgslcblas -lboost_thread -lboost_system $(link)


SRCS= Data.cpp  Lookup.cpp  main.cpp  MyDistribution.cpp  MyModel.cpp  Orbit.cpp
OBJS=$(subst .cpp,.o,$(SRCS))

all: main

%.o: %.cpp
	g++ $(CFLAGS) -c $<


main: $(OBJS)
	#echo $(OBJS)
	g++ -o main $(OBJS) $(LIBS)

clean:
	rm $(OBJS)