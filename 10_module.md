Module is a unit that is responsible of something.
It depends on clients or other modules, and have functionalities.

Common practice is to have a module with the following structure:

```go
type Module interface() {
	Func1(arg1 string, arg2 int) (*Result, error)
	Func2()
	...
}

// Config contains all module dependencies
type Config struct {
	// config members should be eigher interfaces, not concrete struct with functions:
	C1 client1.Client
	C2 client2.Client
  
	// or configuration variables, with no functionalities.
	Timeout time.Duration
  
	// a module logger is always nice to have.
	Log log.Logger
}

// New returns the interface implemented by this package, it actually initiate a module instance.
func New(c Config) Module {
	return &module{Config: Config}
}

// module is a private struct that implements the Module interface and uses the Config to do so.
type module struct {
	Config
}

// Now module should implements interface Module:

func (m *module) Func1(arg1 string, arg2 int) (*Result, error) {
}

func (m *module) Func2() {
}
```