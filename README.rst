Alchemytools
------------

This project brings a set of useful tools to be used in any SQLAchemly project.

The idea is to save common problems, for example: Opening/Closing sessions, commiting the sesssin only at the end of the transaction, etc.


Available Tools
###############

Here are all tools available in alchemytools.

Context Managers
****************

managed
=======

This is the basic context manager and it will commit and close your session automatically, at the end of the ``with`` block.

      ::

            with managed(MySessionClass) as session:
                # Do what you need with your session
            # Here the session is already closed and commited
            
If you raise any exception inside the ``with`` block, the session will be rolled back and the exception re-raised.

To avoid having all of the function body inside the ``with`` block, ``managed`` functions as a context manager as well.

      ::

            @managed(MySessionClass)
            def foo(session, *args, **kwargs):
                # Do what you need with your session
                pass


            # call as if the session didn't exist:
            foo(2, a='b')

The session is opened every time the function is called and closed whenever it returns or raises an exception. Autommit and rollback rules work as normal.

Additional options
^^^^^^^^^^^^^^^^^^
   
 * ``auto_flush``: Sets the autoflush option on the SQLAlchemy session, defaults fo ``False``
