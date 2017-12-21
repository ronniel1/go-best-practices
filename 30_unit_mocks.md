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
u := new(unit.MockAPI)
u.On("Func1").Return().Once()
// ...
u.AssertExpectations(t)
```
