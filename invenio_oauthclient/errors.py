# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2014, 2015, 2016, 2017 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Module level errors."""


class AlreadyLinkedError(Exception):
    """Signifies that an account was already linked to another account."""

    def __init__(self, user, external_id):
        """Initialize exception."""
        self.user = user
        self.external_id = external_id


class OAuthError(Exception):
    """Base class for OAuth exceptions."""

    def __init__(self, message, remote):
        """Initialize exception.

        :param message: Error message.
        :param message: Remote application.
        """
        self.message = message
        self.remote = remote


class OAuthResponseError(OAuthError):
    """Define response exception during OAuth process."""

    def __init__(self, message, remote, response):
        """Initialize exception.

        :param message: Error message.
        :param remote: Remote application.
        :param response: OAuth response object.
        """
        super(OAuthResponseError, self).__init__(message, remote)
        self.response = response


class OAuthRejectedRequestError(OAuthResponseError):
    """Define exception of rejected response during OAuth process."""


class OAuthClientError(OAuthResponseError):
    """Define OAuth client exception.

    Client errors happens when the client (i.e. Invenio) creates an invalid
    request.
    """

    def __init__(self, message, remote, response):
        """Initialize exception.

        :param message: Error message.
        :param remote: Remote application.
        :param response: OAuth response object. Used to extract ``error``,
                         ``error_uri`` and ``error_description``.
        """
        # Only OAuth2 specifies how to send error messages
        self.code = response['error']
        self.uri = response.get('error_uri', None)
        self.description = response.get('error_description', None)
        super(OAuthClientError, self).__init__(
            self.description or message, remote, response
        )
