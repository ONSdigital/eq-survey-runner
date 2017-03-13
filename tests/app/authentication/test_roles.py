import sys
from unittest import TestCase
from mock import patch
from werkzeug.exceptions import Forbidden


class TestRoleRequired(TestCase):

    def setUp(self):
        # Create a patched get_metadata
        self.get_metadata_patcher = patch('app.globals.get_metadata', autospec=True)
        self.addCleanup(self.get_metadata_patcher.stop)
        self.mock_get_metadata = self.get_metadata_patcher.start()

        # Create a patched current_user
        self.get_current_user_patcher = patch('flask_login.current_user', autospec=True)
        self.addCleanup(self.get_current_user_patcher.stop)
        self.mock_current_user = self.get_current_user_patcher.start()

        # Between tests we have to remove the imported module
        # otherwise the Mocks for get_metadata and current_user
        # are cached and can't be replaced.
        if 'app.authentication.roles' in sys.modules:
            del sys.modules['app.authentication.roles']

        # The import of app.authentication.roles.role_required must be
        # performed after get_metadata and current_user have been patched
        # otherwise the original functions are cached and not patched correctly
        from app.authentication.roles import role_required
        self.role_required = role_required

    def test_role_required_unauthenticated_no_metadata(self):
        # Given I am not authenticated and have no metadata
        self.mock_get_metadata.return_value = None
        self.mock_current_user.is_authenticated = False

        # And I have decorated a function with role_required
        wrapper = self.role_required('dumper')
        wrapped_func = wrapper(lambda: 'not called')

        # When I call the decorated function
        # Then a Forbidden exception is raised
        with self.assertRaises(Forbidden):
            wrapped_func()

    def test_role_required_authenticated_no_metadata(self):
        # Given I am authenticated but have no metadata
        self.mock_get_metadata.return_value = None
        self.mock_current_user.is_authenticated = True

        # And I have decorated a function with role_required
        wrapper = self.role_required('dumper')
        wrapped_func = wrapper(lambda: 'not called')

        # When I call the decorated function
        # Then a Forbidden exception is raised
        with self.assertRaises(Forbidden):
            wrapped_func()

    def test_role_required_authenticated_with_empty_metadata(self):
        # Given I am authenticated but my metadata is empty
        self.mock_get_metadata.return_value = {}
        self.mock_current_user.is_authenticated = True

        # And I have decorated a function with role_required
        wrapper = self.role_required('dumper')
        wrapped_func = wrapper(lambda: 'not called')

        # When I call the decorated function
        # Then a Forbidden exception is raised
        with self.assertRaises(Forbidden):
            wrapped_func()

    def test_role_required_authenticated_with_metadata_none_roles(self):
        # Given I am authenticated but my metadata contains a
        # roles list set to None
        self.mock_get_metadata.return_value = {'roles': None}
        self.mock_current_user.is_authenticated = True

        # And I have decorated a function with role_required
        wrapper = self.role_required('dumper')
        wrapped_func = wrapper(lambda: 'not called')

        # When I call the decorated function
        # Then a Forbidden exception is raised
        with self.assertRaises(Forbidden):
            wrapped_func()

    def test_role_required_authenticated_with_metadata_empty_roles(self):
        # Given I am authenticated and my metadata contains an empty
        # roles list
        self.mock_get_metadata.return_value = {'roles': []}
        self.mock_current_user.is_authenticated = True

        # And I have decorated a function with role_required
        wrapper = self.role_required('dumper')
        wrapped_func = wrapper(lambda: 'not called')

        # When I call the decorated function
        # Then a Forbidden exception is raised
        with self.assertRaises(Forbidden):
            wrapped_func()

    def test_role_required_authenticated_with_metadata_wrong_role(self):
        # Given I am authenticated and my metadata contains a single role.
        self.mock_get_metadata.return_value = {'roles': ['flusher']}
        self.mock_current_user.is_authenticated = True

        # And I have decorated a function with role_required, specifying a
        # role that isn't in the metadata roles list.
        wrapper = self.role_required('dumper')
        wrapped_func = wrapper(lambda: 'not called')

        # When I call the decorated function
        # Then a Forbidden exception is raised
        with self.assertRaises(Forbidden):
            wrapped_func()

    def test_role_required_authenticated_with_metadata_matching_role(self):
        # Given I am authenticated and my metadata contains a single role.
        self.mock_get_metadata.return_value = {'roles': ['dumper']}
        self.mock_current_user.is_authenticated = True

        # And I have decorated a function with role_required, specifying a
        # role that is listed in the metadata roles list.
        wrapper = self.role_required('dumper')
        wrapped_func = wrapper(lambda: 'single was called')

        # When I call the decorated function
        # Then the function is executed and returns a value
        self.assertEqual(wrapped_func(), 'single was called')

    def test_role_required_authenticated_with_metadata_matching_multiple_role(self):
        # Given I am authenticated but my metadata contains multiples roles
        self.mock_get_metadata.return_value = {'roles': ['flusher', 'other', 'dumper']}
        self.mock_current_user.is_authenticated = True

        # And I have decorated a function with role_required, specifying a
        # role that is listed in the metadata roles list.
        wrapper = self.role_required('other')
        wrapped_func = wrapper(lambda: 'other was called')

        # When I call the decorated function
        # Then the function is executed and returns a value
        self.assertEqual(wrapped_func(), 'other was called')

    def test_role_required_wrapped_with_positional_arguments(self):
        # Given I am authenticated and my metadata contains roles
        self.mock_get_metadata.return_value = {'roles': ['flusher', 'other', 'dumper']}
        self.mock_current_user.is_authenticated = True

        # And I have decorated a function that takes multiple positional arguments
        # with role_required, specifying a role that is listed in the metadata
        # roles list.
        wrapper = self.role_required('other')
        wrapped_func = wrapper(lambda arg1, arg2, arg3: [arg1, arg2, arg3])

        # When I call the decorated function with arguments
        # Then the function is executed and returns the arguments supplied
        self.assertListEqual(wrapped_func(1, 2, 3), [1, 2, 3])

    def test_role_required_wrapped_with_keyword_arguments(self):
        # Given I am authenticated and my metadata contains roles
        self.mock_get_metadata.return_value = {'roles': ['flusher', 'other', 'dumper']}
        self.mock_current_user.is_authenticated = True

        # And I have decorated a function that takes multiple positional arguments
        # with role_required, specifying a role that is listed in the metadata
        # roles list.
        wrapper = self.role_required('other')
        wrapped_func = wrapper(lambda arg1=None, arg2=None: [arg1, arg2])

        # When I call the decorated function with arguments
        # Then the function is executed and returns the arguments supplied
        self.assertListEqual(wrapped_func(arg1='y', arg2='z'), ['y', 'z'])

    def test_role_required_wrapped_with_positional_and_keyword_arguments(self):
        # Given I am authenticated and my metadata contains roles
        self.mock_get_metadata.return_value = {'roles': ['flusher', 'other', 'dumper']}
        self.mock_current_user.is_authenticated = True

        # And I have decorated a function that takes multiple positional arguments
        # with role_required, specifying a role that is listed in the metadata
        # roles list.
        wrapper = self.role_required('other')
        wrapped_func = wrapper(lambda arg1, arg2=None: [arg1, arg2])

        # When I call the decorated function with both positional and keyword arguments
        # Then the function is executed and returns the arguments supplied
        self.assertListEqual(wrapped_func('i', arg2=2), ['i', 2])

    def test_role_required_unauthenticated_wrapped_with_arguments(self):
        # Given I am not authenticated
        self.mock_get_metadata.return_value = {}
        self.mock_current_user.is_authenticated = False

        # And I have decorated a function that takes multiple arguments
        wrapper = self.role_required('other')
        wrapped_func = wrapper(lambda arg1, arg2, arg3: [arg1, arg2, arg3])

        # When I call the decorated function with arguments
        # Then a Forbidden exception is raised
        with self.assertRaises(Forbidden):
            wrapped_func('a', 'b', 'c')

    def test_role_required_unauthenticated_wrapped_with_keyword_arguments(self):
        # Given I am not authenticated
        self.mock_get_metadata.return_value = {'roles': ['flusher', 'other', 'dumper']}
        self.mock_current_user.is_authenticated = False

        # And I have decorated a function that takes multiple positional arguments
        # with role_required, specifying a role that is listed in the metadata
        # roles list.
        wrapper = self.role_required('other')
        wrapped_func = wrapper(lambda arg1=None, arg2=None: [arg1, arg2])

        # When I call the decorated function with keyword arguments
        # Then a Forbidden exception is raised
        with self.assertRaises(Forbidden):
            wrapped_func(arg1='y', arg2='z')

    def test_role_required_unauthenticated_wrapped_with_positional_and_keyword_arguments(self):
        # Given I am not authenticated
        self.mock_get_metadata.return_value = {'roles': ['flusher', 'other', 'dumper']}
        self.mock_current_user.is_authenticated = False

        # And I have decorated a function that takes multiple positional arguments
        # with role_required, specifying a role that is listed in the metadata
        # roles list.
        wrapper = self.role_required('other')
        wrapped_func = wrapper(lambda arg1, arg2=None: [arg1, arg2])

        # When I call the decorated function with keyword arguments
        # Then a Forbidden exception is raised
        with self.assertRaises(Forbidden):
            wrapped_func('p', arg2=9)
