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

Additional options
^^^^^^^^^^^^^^^^^^
   
 * ``auto_flush``: Sets the autoflush option on the SQLAlchemy session, defaults fo ``False``


commit_on_success
=================

This contextmanager should be used in an inner ``with`` block, where you already have an open session but need to commit more than one time. The code will be something on these lines.

  ::

    with managed(MySession) as session:
        for a in iterable:
            with commit_on_success(session):
                process(a)
                session.add(a)

If you raise an exception inside the second ``with`` block, all previous iterations will already be commited and just the current one will be rolledback.
