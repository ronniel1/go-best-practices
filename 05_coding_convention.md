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
