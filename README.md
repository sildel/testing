# testing
This project is a web site implemented with Flask framework, Jquery and Bootstrap.

This website is used to make supervission and control of a RPi controlled robot. It uses websockets to update the client browser and AJAX request to control the robot. The server runs threads and sockets to communicate with the controller service/process of the robot that runs in the RPi. This webserver is currently working on the RPi but it could be moved out to a different PC since it uses sockets send orders and receive status of the robot.
