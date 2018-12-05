from pubsub import Store


default_state = {
    'firstname': '',
    'lastname': '',
    'age': 0,
    'country': ''
}

def test_reducer(state, action):
    if not state: state = default_state

    if action['type'] == 'firstname':
        return { **state, 'firstname': action['payload'] }

    if action['type'] == 'lastname':
        return { **state, 'lastname': action['payload'] }

    if action['type'] == 'age':
        return { **state, 'age': action['payload'] }

    if action['type'] == 'country':
        return { **state, 'country': action['payload'] }

    return state

def logger_middleware(store):
    def mw_dispatch(dispatch):
        def new_dispatch(action):
            print('Action: ', action)
            dispatch(action)
            print('State: ', store.getState())
        return new_dispatch
    return mw_dispatch


store = Store(test_reducer, default_state, [logger_middleware])

def log_state(state):
    if state['age'] < 21:
        print("You can't drink")
    else:
        print("You can drink!")

store.subscribe(log_state)

store.dispatch({
    'type': 'age',
    'payload': 99
})

store.dispatch({
    'type': 'firstname',
    'payload': 'J'
})

store.dispatch({
    'type': 'lastname',
    'payload': 'Doe'
})

store.dispatch({
    'type': 'country',
    'payload': 'U.S.A.'
})
