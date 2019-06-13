# Stratoscale Go Best Practices

Here is a link to the [discussion video](https://drive.google.com/a/stratoscale.com/file/d/13qoSDfqmoEHpB9Xw_cP_dJv6NGuIdX3G/view?usp=sharing).

# TOC

* [Main](#main)
* [Coding convention](#coding-convention)
* [Unit](#unit)
* [Unittests](#unittests)
* [Unit mocks](#unit-mocks)
* [Logging](#logging)
* [Flow](#flow)
* [Naming](#naming)
* [3rd party pkgs](#3rd-party-pkgs)




# Main

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

# Coding convention

## Structs
When initializing a struct, explicitly define the key names that you're setting:

```go
Person{Name:"John Doe", Address:"New York"}
```

This is so when the Struct changes, your code will still compile
```go
type Person struct {
    Name    string
    Address string
    Age     int
}
Person{Name:"John Doe", Address:"New York"}  // Compiles
Person{"John Doe", "New York"}               // Doesn't compile!
```
Notice even though the "Age" attribute was added to the end of the struct, the compilation still fails - it expects to have the exact number of attribute on initialation.


# Unit

Unit is a part of your application that responsible to do something.
It holds state (or may be stateless), and exposes some functionality (its behavior).
To accomplish that, it may uses (depends) on zero or more units.

Common practice is to have a file in the following structure:

```go

//go:generate mockery -name API -inpkg

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


// unit is a unit that implements the interface above and uses the Config to do so.
type unit struct {
	Config

	// unit's state.
	blocks chan<-uint
}

// New returns the unit that exposed by this file (or package).
//
// Other units that depend on this behavior, may use its interface on
// their dependency list (like the config struct above).
func New(c Config) (API, error) {
	// Validate requirements, or use default values.
	if c.C1 == nil {
		return nil, fmt.Errorf("must give client1")
	}
	// Return the constructed type
	return &unit{
		Config: c,
		blocks: make(chan uint),
	}, nil
}
```


# Unittests

For each public unit function, we usually want to create a unittest, that tests all the flows in the function code.

* Table driven tests
* All unit dependencies are mocks

a unittest for `Func1(arg1 string, arg2 int) (*Result, error)` will look like:

```go
func TestUnit_Func1(t *testing.T) {
	t.Parallel()
	
	tests = []struct{
		name string // name for test case
		arg1 string
		arg2 int
		want *Result
		wantError bool
		prepare func(*client1.Mock, *client2.Mock)
	}{
		{
			// test 1
			name: "simple input",
			arg1: "a",
			arg2: 1,
			want: &Result{Concat: "a1"},
			wantErr: false,
			prepare: func(c1 *client1.Mock, c2 *client2.Mock) {
				// here we prepare the mocks that the unit are dependent on.
				c1.On("Check", mock.Anything).Return(nil).Once()
				c2.On("Add", "a", 1).Return("a1", nil).Once()
				// ...
			},
		},
		{
			// test 2
		},
		// ...
	}
	
	for _, tt := range tests {
		// constract a unique name for the test, from the function arguments
		name := fmt.Sprintf("%s,%d", tt.arg1, tt.arg2)
		
		// run a sub-test:
		t.Run(name, func(t *testing.T) {
			// create mocks
			c1 := new(client1.Mock)
			c2 := new(client2.Mock)
			
			// prepare the mocks:
			if tt.prepare != nil {
				tt.prepare(c1, c2)
			}
			
			log := log.New("test")
			if !t.Verbose() {
				log.Out = ioutil.Discard
			}
			
			// create unit
			u, err := New(&Config{
				Log:     log,
				Client1: c1,
				Client2: c2,
			})
			require.Nil(t, err) // notice require and not assert - will fail the test immediatly.
			
			// run the tested function
			got, err := u.Func1(tt.arg1, tt.arg2)
			
			// assert results expectations
			if tt.wantErr {
				assert.NotNil(t, err)
			} else {
				assert.Nil(t, err)
				assert.Equal(t, want, got) // notice the go convention: want is first argument, got is the second argument
			}
			
			// assert that the mocks were called correctly.
			c1.AssertExpectations(t)
			c2.AssertExpectations(t)
		})
	}
}
```


# Unit mocks

Each unit should expose it's mocking object.

We use [testify/mock](https://github.com/stretchr/testify#mock-package).

A usefull tool that can be applied with the `go generate` command is the [mockery tool](https://github.com/vektra/mockery).

Just add above each interface that the unit expose the `go:generate` comment:

```go
//go:generate mockery -name API -inpkg

// API is ....
type API interface {
	Func1()
	// ...
}
```

This will generate a file named mock_API.go with a struct `MockAPI`, which is exported by the `unit` package.
Other packages which use the `unit.API` interface can use this mock in their unittests:

```go
u1 := new(unit1.MockAPI)
u1.On("Func1").Return().Once()
// ...
u1.AssertExpectations(t)
```
Since we are using "dependency injection", another unit (`unit2`) gets `unit1` in it's config, and in it's unittests
it could get a mock:

In `unit2` package:
```go
u1 := new(unit1.MockAPI)
u1.On("Func1").Return().Once()

u2 := New(Config{U1: u1})

got := u2.Func1()
assert.Equal(t, want, got)

u.AssertExpectations(t)
```


# Logging

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


# Flow

### Avoid nested error handling

Bad:
```go
f, err := os.Open(name)
if err == nil {
  b, err := ioutil.ReadAll(f)
  if err == nil {
    // ...
  }
}
```

Good:
```go
f, err := os.Open(name)
if err != nil {
  return err
}
b, err := ioutil.ReadAll(f)
if err != nil {
  return err
}
// ...
```


### Embrace the switch statement

Bad:
```go
r := read()
if r >= '0' && r <= '9' {
  // ...
} else if r >= 'a' && r <= 'z' {
  // ...
} else if r >= 'A' && r <= 'Z' {
  // ...
} else {
  // ...
}
```
Good:

```go
switch r := read(); {
case r >= '0' && r <= '9':
  // ...
case r >= 'a' && r <= 'z':
  // ...
case r >= 'A' && r <= 'Z':
  // ...
default:
  // ...
}
```

### Use Anonymous structs instead of `map[string]interface{}` ("dict" for Python developers).
Cheaper and safer than using `map[string]interface{}`.
```go
games1 := map[string]Game{
  "dino":   dino.New(),
  "snake":  snake.New(),
  "tetris": tetris.New(),
}

// This one is prefered.
games2 := struct{
  Dino, Snake, Tetris Game
}{
  Dino:   dino.New(),
  Snake:  snake.New(),
  Tetris: tetris.New(),
}

games1["tetris"].Play() // :(
games2.Tetris.Play()    // :)
```



# Naming

### Good names are:
- Consistent (easy to guess),
- Short (easy to type),
- Accurate (easy to understand).

### A rule of thumb
The greater the distance between a name's declaration and its uses, 
the longer the name should be.

### Use MixedCase
Don't use snake_case.

## Local variables
Keep them short. long names obscure what the code does.  
Common variable/type combinations may use really short names:
- Prefer `i` to index. 
- Prefer `r` to reader. 
- Prefer `b` to buffer.

Bad:
```go
func countBufferRunes(buffer []byte) {
  runeCount := 0
  for idx := range buffer {
    // ...
  }
}
```

Good:
```go
func runeCount(b []byte) {
  count := 0
  for i := range b {
    // ...
  }
}
```
Function parameters are like local variables, 

### Return values
Return values on exported functions should only be named for documentation purposes.

These are good examples of named return values:
```go
func Copy(dst Writer, src Reader) (written int64, err error)
```

### Receivers
Receiver names should be consistent across a type's methods.  
Don't use `this` or `self` for receiver names.  

```go
func (this *Buffer) RuneCount() int {}                                // bad
func (b *Buffer) Read(p []byte) (n int, err error) {}                 // good
func (sh serverHandler) ServeHTTP(rw ResponseWriter, req *Request) {} // good
```

### Constants
```go
const PI = 3.14 // bad
const Pi = 3.14 // good
```

### Errors
Errors
Error types should be of the form FooError:
```go
type ExitError struct {
    ...
}
```
Error values should be of the form ErrFoo:
```go
var ErrFormat = errors.New("image: unknown format")
```

### Test naming
Emphasize the role of what you are testing rather than naming after the inputs and outputs.
```go
func TestTitleIllegalChar(t *testing.T) {} // bad
func TestTitleEscape(t *testing.T) {}      // good
```

### Packages
Organize by responsibility.  
A common practice from other languages is to organize types together in a package called models or types.  
Bad:
```go
package models // DON'T DO IT!!!

// User represents a user in the system.
type User struct { }
```
Rather than creating a models package and declare all entity types there,
a User type should live in a service-layer package.  

Good:
```go
package mngtservice

// User represents a user in the system.
type User struct {...}

func UsersByQuery(ctx context.Context, q *Query) ([]*User, *Iterator, error) {}

func UserIDByEmail(ctx context.Context, email string) (int64, error) {}
```


### Package Naming
- Lowercase only.  
  Package names should be lowercase. Don’t use snake_case or camelCase in package names.
  [Link to Go blog](https://blog.golang.org/package-names)
- Short, but representative names.  
  Avoid overly broad package names like “common” and “util”.
  ```go
    import "pkgs.org/common" // DON'T!!!
  ```
- No plurals.  
  In Go, package names are not plural.
  ```go
  package httputils // bad
  package httputil  // good
  ```

#### Credit and links
- https://talks.golang.org/2014/names.slide#1
- https://blog.golang.org/package-names
- https://rakyll.org/style-packages/




# 3rd party pkgs

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
