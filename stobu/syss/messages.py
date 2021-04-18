"""Define message templates."""

# Official Libraries


# My Modules


# Process messages
PROC_START = '> Starting {proc} ...'

PROC_SUCCESS = '___{proc} Successfull.'

PROC_DONE = '... {proc} ...DONE.'

PROC_DONE_WITH_DATA = '... {proc} ...DONE: %s'

PROC_INITIALIZED = '... {proc} Initialized.'

PROC_MESSAGE = '... {proc}.'

PROC_FAILED = '!!! {proc} Failed!!!'

MSG_ALREADY_EXISTS_DATA = '... {data} Already Exists.'

# Error messages
ERR_FAILED_PROC = '! Failed {proc}!'

ERR_FAIL_CANNOT_CREATE_DATA = '! Failed. Cannot create {data}!'

ERR_FAIL_CANNOT_CREATE_DATA_WITH_DATA = '! Failed Cannot create {data}!: %s'

ERR_FAIL_CANNOT_INITIALIZE = '! Failed. Cannot initialize {data}!'

ERR_FAIL_CANNOT_INITIALIZE_WITH_DATA = f"{ERR_FAIL_CANNOT_INITIALIZE}: %s"

ERR_FAIL_CANNOT_REMOVE_DATA = '! Failed Cannot remove {data}!'

ERR_FAIL_CANNOT_REMOVE_DATA_WITH_DATA = '! Failed Cannot remove {data}!: %s'

ERR_FAIL_CANNOT_WRITE_DATA = '! Failed Cannot write {data}!'

ERR_FAIL_CANNOT_WRITE_DATA_WITH_DATA = '! Failed Cannot write {data}!: %s'

ERR_FAIL_DUPLICATED_DATA = '! Failed. Duplicated {data}!'

ERR_FAIL_DUPLICATED_DATA_WITH_DATA = '! Failed. Duplicated {data}!: %s'

ERR_FAIL_INVALID_DATA = '! Failed Invalid {data}!'

ERR_FAIL_INVALID_DATA_WITH_DATA = '! Failed Invalid {data}!: %s'

ERR_FAIL_MISSING_DATA = '! Failed. Missing {data}!'

ERR_FAIL_MISSING_DATA_WITH_DATA = '! Failed. Missing {data}!: %s'

ERR_FAIL_SUBPROCESS = '! Failed Subprocess of {proc}!'

ERR_FAIL_SET_DATA = '! Failed to set {data}!'

ERR_FAIL_SET_DATA_WITH_DATA = '! Failed to set {data}!: %s'

ERR_FAIL_UNKNOWN_DATA = '! Failed. Unknown {data}!'

ERR_FAIL_UNKNOWN_DATA_WITH_DATA = '! Failed. Unknown {data}! %s'
