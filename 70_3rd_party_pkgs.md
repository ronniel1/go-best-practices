## A list of packages we widly use:

* [gorm](https://github.com/jinzhu/gorm) - most popular package for ORM
* [go-swagger](https://github.com/go-swagger/go-swagger) - Generates code for a swagger file.
  - We have mixed feelings about this generator. It wrapps too many things, and annoying pointers 
    notation in the generated models when a field is "required".
  - We use the generated model and http handler.
  - We don't use the generated server.
  - The client is also so-so, maybe we should find a better client generator.
* [aws go sdk](https://github.com/aws/aws-sdk-go) - Use the `iface` package for each service!
* [testify](https://github.com/stretchr/testify) - Very good and comfortable for unittesting and mocks.
  Currently it's not longer active, probably will be moved to another organization.
  - [Issue](https://github.com/stretchr/testify/issues/526).
  - [New repo](https://github.com/test-go/testify)
* [logrus](https://github.com/sirupsen/logrus) - for logging.
