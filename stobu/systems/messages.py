"""Define various message templates."""

# Official Libraries


# My Modules


# Application messages
MSG_INITIALIZED = '> Initialized {app}.'

MSG_START_APP = '> Starting {app}...'

MSG_FINISH_APP = '> ...Finished {app}.'

MSG_SUCCESS_PROC = '> ...Succeeded {proc}.'

MSG_SUCCESS_PROC_WITH_DATA = '> ...Succeeded {proc}: %s'

# Error messages
ERR_FAILURE_APP_INITIALIZED = '! Failed to initialize {app}!'

ERR_FAILURE_PROC = '! Failed {proc}!'

ERR_FAILURE_PROC_WITH_DATA = '! Failed {proc}!: %s'

ERR_MISSING_DATA = '! Missing {data}!: %s'

ERR_UNKNOWN_PROC = '! Unknown {proc}!'

ERR_UNKNOWN_PROC_WITH_DATA = '! Unknown {proc}!: %s'
