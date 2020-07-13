We use [golang/mock](https://github.com/golang/mock).

A Useful tool that can be applied with the `go generate` command is the
[mockgen](https://github.com/golang/mock#running-mockgen).

Just add above each interface that the unit expose the `go:generate` comment:

```go
//go:generate mockgen -package=<package-name> -destination mock_api.go . API

// API is ....
type API interface {
	Func1()
	// ...
}
```

This will generate a file named mock_API.go with a struct `MockAPI`, which is exported by the `unit` package.
Other packages which use the `unit.API` interface can use this mock in their unittests:

```go
ctrl := gomock.NewController(GinkgoT())
u1 := util.NewMockAPI(ctrl)
u1.EXPECT.Func1.Return().Times(1)
// ...
ctrl.Finish()
```
Since we are using "dependency injection", another unit (`unit2`) gets `unit1` in it's config, and in it's unittests
it could get a mock:

In `unit2` package:
```go
ctrl := gomock.NewController(GinkgoT())
u1 := util.NewMockAPI(ctrl)
u1.EXPECT.Func1.Return().Times(1)

u2 := New(Config{U1: u1})

got := u2.Func1()
assert.Equal(t, want, got)

ctrl.Finish()
```

Mock third party interface can be done as part of your makefile

```makefile
generate:
    mockgen -destination externalmocks/mock_<filename>.go github.com/<repo>/<dir1>/<dir2>/<package> <interface>
    # example:
    mockgen -package=mockinstaller -destination externalmocks/installer/mock_installer.go github.com/filanov/bm-inventory/client/installer API
```