API Specification
=================

.. toctree::
    :maxdepth: 4
    :caption: API Specification

API Modules
-----------

The API modules are used to provide functionality to the website. This is accomplished by having the API be capable of performing any action on the website. Because of this, the API modules can be imported into any other module that requires API functionality, such as the API endpoints. This allows the site functionality to be exposed to the user and programmer from a single location.

There are currently three API modules.

The :ref:`Admin API<admin_api-label>` contains all administrative features and functions of the site. This module should be used in any section of the site that requires administrative access. The admin API should only be used where adequate checks for administrative access have been performed.

The :ref:`Client API<client_api-label>` contains all functions required for a non-admin user to use the site such as getting play and seating information reserving seats.

The :ref:`Shared API Functions<shared_api-label>` contains functionality that is shared between the Admin and Client APIs. For the most part, this includes functions to get various objects, such as plays, seats, dates, etc. Modification of data should not be handled in this module.

API Endpoints
-------------

The API endpoints are used to expose the API Modules to the outside world (and also to our own website through Javascript). They all work in the following way:

#. HTTP request methods are used to indicate endpoint function:
    * DELETE
    * GET
    * POST
    * PUT
#. All data returned to the requestor is JSON
#. All required input data is in JSON format OR retrievable from the URL (ie: play IDs).

The :ref:`Admin API Endpoints<admin_api_endpoints-label>` expose the Admin API module functions and require authentication to access. The authenticated user must be an administrator on the site to make use of the endpoints.

The :ref:`Client API Endpoints<client_api_endpoints-label>` expose the non-administrative functions of the site, such as allowing logged in users to purchase and reserve a seat at a play.
