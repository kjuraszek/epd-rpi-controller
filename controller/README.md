# EPD RPi Controller backend

EPD RPi Controller backend overview.

## Controller structure

Controller consists of a three key components running as threads in a loop:

- Consumer
- View Manager
- API

and two optional ones: Producer and Button Manager.

### Consumer

Consumer is responsible for consuming messages from Kafka topic and triggering proper actions from View Manager.

### View Manager

View Manager is responsible for running and switching views in a particular order. It also passes views data to the API. Also check [Custom views](/controller/custom_views/README.md) to learn more about views.

### API

API exposes few endpoints which are used by user interface. Swagger documentation is also exposed, by default: [localhost:8888/api/doc/](http://localhost:8888/api/doc/) .

### Producer \[OPTIONAL\]

Producer is responsible for switching views automatically by defined time interval - a "slideshow".

### Button Manager \[OPTIONAL\]

Button Manager allows to use physical buttons connected directly to Raspberry Pi to manipulate views.
