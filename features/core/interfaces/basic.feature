Feature: Basic interfaces

	Interfaces are the main interaction point between the user and a fixture.
	Each feature gives a set of interfaces, associated with a functional feature,
	for example, the dimmer, the color or the position.

	# ┌────────────────────────────────────────┐
	# │ RangeValue Codec                       │
	# └────────────────────────────────────────┘

	Scenario: `RangeValue` serialization
		
		A `RangeValue` interface instance
		can be serialized to a dict.

		Given a `RangeValue` instance with a min of 0.0, a max of 1.0, and a unit of "test"
		When I serialize the instance
		Then The serialized value is "{'min': 0.0, 'max': 1.0, 'unit': 'test'}"


	Scenario: `RangeValue` deserialization
		
		A `RangeValue` interface instance can be deserialized
		from a dict.

		This scenario checks that a `RangeValue` interface
		can be deserialized

		Given a dictionary containing "{'min': 0.0, 'max': 1.0, 'unit': 'test'}"
		When I create an instance of `RangeValue` using the dictionnary
		Then instance's "min" is equal to the number 0.0
		And instance's "max" is equal to the number 1.0
		And instance's "unit" is equal to the string "test"	

	
	# ┌────────────────────────────────────────┐
	# │ RangeValue Set/Get                     │
	# └────────────────────────────────────────┘

	Scenario: `RangeValue` set
		
		A `RangeValue` has two operations, `set` and `get`. The set
		value is checked against the range's limits
		
		TODO
