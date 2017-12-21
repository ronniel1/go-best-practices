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

#### Useful links
- https://talks.golang.org/2014/names.slide#1
- https://blog.golang.org/package-names
- https://rakyll.org/style-packages/


