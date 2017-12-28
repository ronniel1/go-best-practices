For each public module function, we usually want to create a unittest, that tests all the flows in the function code.

* Table driven tests
* All module dependencies are mocks

a unittest for `Func1(arg1 string, arg2 int) (*Result, error)` will look like:

```go
func TestModule_Func1(testing *t.T) {
	t.Parallel()
	
	tests = []struct{
		arg1 string
		arg2 int
		want *Result
		wantError bool
		prepare func(*client1.Mock, *client2.Mock)
	}{
		{
			// test 1
			arg1: "a",
			arg2: 1,
			want: &Result{Concat: "a1"},
			wantErr: false,
			prepare: func(c1 *client1.Mock, c2 *client2.Mock) {
				// here we prepare the mocks that the module are dependent on.
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
			
			// create Module
			m, err := New(&Config{
				Log:     log,
				Client1: c1,
				Client2: c2,
			})
			require.Nil(t, err) // notice require and not assert - will fail the test immediatly.
			
			// run the tested function
			got, err := m.Func1(tt.arg1, tt.arg2)
			
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
