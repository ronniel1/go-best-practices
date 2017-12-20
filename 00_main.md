Usually the main package will be in path `cmd/`. A file `cmd/main.go` will contain the execution of the service,
It consists of:

1. Options parsing
2. Clients/dependencies initializations.
3. Program componenet initializations.
4. Running the program.

## Main Concepts

### Options 

Are concentrated in the `main.go` file, loaded from environment variables.

```go
// options are from environment variables
var options struct {
	// Mysql is root configuration of local mysql server
	Mysql mysql.Config
	Server1Addr      string        `envconfig:"SERVER1_ADDRESS" required:"true"`
	Server2Addr      string        `envconfig:"SERVER2_ADDRESS" required:"true"`
	RequestTimeout   time.Duration `envconfig:"REQUEST_TIMEOUT" default:"10s"`
}
```

We use the [envconfig](https://github.com/kelseyhightower/envconfig) package.
* It supports the main types: int, string, time.Time, time.Duration, etc...
* Supports nesting of structs: see `Mysql` type above.

### Main function:

Main principles:

* Dependencies injection - inject clients into the program componenets.
  Good for unittesting of each module.
* `failOnError`: when main function gets an error, it should fail, the orchestrator will re-run it.

```go
func main() {
	log := log.New()
	
	c1 = client2.Init()
	c2 = client2.Init(options.VirtualIP)
	
	...
	
	m1, err = module1.New(module1.Config{
		Client1: client1,
		Client2: client2,
		Log: log.With("pkg", "module1"),
  	})
	failOnError(err, "initializing module1")
	
	m2, err := module2.New(module2.Config{
		Client2: client2,
		Log: log.With("pkg", "module2"),
  	})
	failOnError(err, "initializing module2")
	...
	
	m1.DoSomething()
	m2.DoSomething()
}
```