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

