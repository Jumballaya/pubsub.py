'''
Pub-Sub state management
'''


'''
Decorate Dispatch
'''
def decorateDispatch(store, base, middleware):
    dispatch = base
    for mw in middleware:
        dispatch = mw(store)(dispatch)
    return dispatch


'''
Pub-Sub Store
'''
class Store(object):

    def __init__(self, reducer, initState, middleware=[]):
        self.state = initState
        self.reducer = reducer
        self.listeners = []
        self.middleware = middleware

        # Set up dispatch
        def _dispatch(action):
            self.state = self.reducer(self.state, action)
            for l in self.listeners: l(self.state)
        dispatch = decorateDispatch(self, _dispatch, self.middleware)
        self.dispatch = dispatch


    def getState(self):
        return self.state

    def subscribe(self, listener):
        self.listeners.append(listener)
        def unsub():
            index = self.listeners.index(listener)
            if index >= 0:
                del self.listeners[index]
        return unsub



'''
Combine Reducer combines reducer functions into a single reducer function
'''
def combineReducers(reducers):
    def reducer(state, action):
        if not state: state = {}
        newState = {}
        for k in reducers:
            newState[k] = reducers[k](state[k], action)
        return newState
    return reducer
