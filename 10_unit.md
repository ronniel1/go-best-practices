Unit is a part of your application that responsible to do something.
It holds state (or may be stateless), and exposes some functionality (its behavior).
To accomplish that, it may uses (depends) on zero or more units.

Common practice is to have a file in the following structure:

```go

type API interface {
	Func1(arg1 string, arg2 int) (*Result, error)
	Func2()
	...
}

// Config holds all unit dependencies
type Config struct {
	// config members should be either interfaces, not concrete struct with functions:
	C1 client1.Client
	C2 client2.Client

	// or configuration variables, with no functionalities.
	Timeout time.Duration

	// Logger is also a dependecy.
	Log log.Logger
}


// Unit is a unit that implements the interface above and uses the Config to do so.
type Unit struct {
	Config

	// Unit's state.
	blocks chan<-uint
}

// New returns the unit that exposed by this file (or package).
//
// Other units that depend on the behavior, may use its interface on
// their dependency list (like the config struct above).
func New(c Config) (*Unit, error) {
	// Validate requirements, or use default values.
	if c.C1 == nil {
		return nil, fmt.Errorf("must give client1")
	}
	// Return the constructed type
	return &Unit{
		Config: Config
		blocks: make(chan uint),
	}, nil
}
```
