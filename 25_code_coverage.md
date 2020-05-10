Not required, but it's nice to know how to check your code coverage. Go have a builtin tools for code coverage [here](https://blog.golang.org/cover)
Those tools can display coverage with a friendly web page.

Store coverage output to file.
```shell script
go test -v -coverprofile=coverage.out
```

Display coverage in a browser.
```shell script
go tool cover -html=coverage.out
```

Single command that run the test show the coverage and clear the file for a specific directory.
```shell script
go test -v -coverprofile=coverage.out && go tool cover -html=coverage.out && rm coverage.out
```

`go test` have maybe options to run specific tests or multiple directories so this command can be used in various ways.

