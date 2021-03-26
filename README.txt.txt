0. Justin Rhodes (jgr85), Greg Fuerte (grf27)

1. For our project, we opted to use a timeout with our sockets to support the LS functionality. For each query the LS deals with, it would go through a try->except->else statement for both TS servers. After sending the query to both TS servers, the LS would 'try' to receive a response from either TS servers. Since we were using timeout sockets, if a TS server did not send back data, then .recv will throw a socket error. The LS would detect this socket error via 'except' and based on the error message, we can tell the socket timed out because the error message would equal "timed out". Otherwise, 'else' would detect if a response were received from either TS servers. To determine which TS server it came from, we simply created two variables: msg1 and msg2 that would recv from ts1 or ts2, respectively. Since it was safe to assume that at most one TS server would have the data we needed, then we knew either msg1 or msg2 would have the data we needed OR both msg1 and msg2 would be empty.

2. Currently, there are no known issues or bugs in our attached code.

3. The most prominent hardship we had for this project was deciding what would be the best approach to dealing with the LS-TS relationship given the constraints. Since we were prohibited from sending "NOT FOUND" messages from either TS servers to the LS, we had to decide how to best approach this. We came up with the idea of either using non-blocking sockets or using timeouts. At this point, it was trial and error to figure out which method would work best. 

4. From this project, we learned how to properly implement a load-balancing server that can figure out which TS server has pushed data into its corresponding socket and timing out when neither has pushed data. We also learned when the most appropriate time is to use a blocking over a non-blocking socket and vice-versa. Overall, this project gave us hands on experience on how a load balancer interacts with clients and how it splits sets of hostnames across multiple DNS servers.

To Run Use Command Lines:
python ts1.py ts1ListenPort
python ts2.py ts2ListenPort
python ls.py lsListenPort ts1Hostname ts1ListenPort ts2Hostname ts2ListenPort
python client.py lsHostname lsListenPort

This Zip File Should Include:
client.py
ls.py
ts1.py
ts2.py
README.txt
