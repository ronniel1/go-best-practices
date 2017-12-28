We use structured logging.
Our library logger github.com/Stratoscale/golib/log wraps [logrus](https://github.com/sirupsen/logrus) logger.

The logger is configured to write structured log (json) to a file, and human readable log to stdout.

We want to get red of it. It wraps the logrus logger functionality, which is not needed. 
Maybe leave only the basic configuration in the library.

* Get logger by interfaces, not the concrete type.
* Don't put everything in a key-value pairs, We prefer more informative messages, and 
  to use key-value for things that could be plotted into a graph.
  
  Example for things that could be plotted:
  - HTTP status code
  - Durations
  - Counters
  
  Things that are less good to be given in a key-value:
  - Arguments, configurations
  - Content of requests, files
  
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
