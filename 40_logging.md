We use structured logging using [logrus](https://github.com/sirupsen/logrus) logger.

The logger is configured to write structured log (json) to a file, and human readable log to stdout.

* Get logger by interfaces, not the concrete type.
  When getting logger as an argument, or holding in in a structure, user the logrus.FieldLogger interface
* Don't put everything in a key-value pairs, We prefer more informative messages, and 
  to use key-value for things that could be plotted into a graph.
  
  Example for things that could be plotted:
  - HTTP status code
  - Durations
  - Counters
  
  Things that are less good to be given in a key-value:
  - Arguments, configurations
  - Content of requests, files
* Logger should be created and initialize in the begining of the ```main``` function
  and should be passed to components as dependency injection.
  Components should accept the FieldLogger as a parameter and store it in their internal structure, for later usage.
  When passing a logger to a newly created component, we should pass a new FieldLogger with the key of 'pkg' which is assigned the package name:
  ```go
  c := NewComponent(log.WithField("pkg", <pkg-name>), ...)
  ```
* When using the logger from a method that gets a ```Context```, the logger should be   enriched by the data in the context using the functionality from our internal [log  helper package](github.com/filanov/bm-inventory/pkg/log), as follows:
  ```go
  import (
    logutil "github.com/filanov/bm-inventory/pkg/log"
  )

  ...

  func (i MyInterface) foo() {
    log := logutil.FromContext(ctx, i.log)
  }
  ```
  This enriches the logs with extra data from the context, such as request-id, if present
* Errors should be logged only in 1 place
  ### DON'T LOG ERROR AND THEN RETURN IT. Errors should be "treated once!"

  Thats wrong:

  ```go
  if err != nil {
	  s.Log.WithError(err).Error("Failed!")
	  return err
  }
  ```

  Either:

  ```go
  if err != nil {
	  return fmt.Errorf("my function failed: %s", err)
  }
  ```

  Or:

  ```go
  if err != nil {
	  s.Log.WithError(err).Error("Failed!")
	  return nil
  }
  ```
