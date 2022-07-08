.. _`shared_api-label`:

Shared API Functionality
========================

Some functionality is shared between the client and admin APIs. For example, it seemed ludicrous to implement a get_play() function in both when it is literally the same thing in both. Not only would it be easy to forget to update one (thus causing breaking changes), it could lead to headaches trying to diagnose where a problem has occurred.

Because of this, some specific shared functionality has been placed in a separate file that can be imported if need be.

.. toctree::
    :maxdepth: 4
    :caption: Shared API Functions

.. automodule:: theatre.routes.api.shared
    :members:
