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

* Dependencies injection - inject clients into the program components.
  Good for unittesting of each unit.
* `failOnError`: when main function gets an error, it should fail, the orchestrator will re-run it.

```go

var log = log.New('my-application')

func main() {
	c1 = client2.Init()
	c2 = client2.Init(options.VirtualIP)
	
	...
	
	u1, err = unit1.New(unit1.Config{
		Client1: c1,
		Client2: c2,
		Log: log.With("pkg", "unit1"),
  	})
	failOnError(err, "initializing unit1")
	
	u2, err := unit2.New(unit2.Config{
		Client2: c2,
		Log: log.With("pkg", "unit2"),
  	})
	failOnError(err, "initializing unit2")
	...
	
	u1.DoSomething()
	u2.DoSomething()
}

func failOnError(err error, msg string) {
	if err == nil {
		return
	}
	log.WithError(err).Fatal(msg)  // causes the program to exit
}
```