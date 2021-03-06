# -*- test-case-name: cyclone.tw.test -*-
# Copyright (c) 2008-2009 Twisted Matrix Laboratories.
# See LICENSE for details.

"""
Interface definitions for L{cyclone.tw}.

@var UNKNOWN_LENGTH: An opaque object which may be used as the value of
    L{IBodyProducer.length} to indicate that the length of the entity
    body is not known in advance.
"""

from zope.interface import Interface, Attribute

from twisted.internet.interfaces import IPushProducer
#from twisted.cred.credentials import IUsernameDigestHash


class IRequest(Interface):
    """
    An HTTP request.

    @since: 9.0
    """

    method = Attribute("A C{str} giving the HTTP method that was used.")
    uri = Attribute(
        "A C{str} giving the full encoded URI which was requested (including "
        "query arguments).")
    path = Attribute(
        "A C{str} giving the encoded query path of the request URI.")
    args = Attribute(
        "A mapping of decoded query argument names as C{str} to "
        "corresponding query argument values as C{list}s of C{str}.  "
        "For example, for a URI with C{'foo=bar&foo=baz&quux=spam'} "
        "for its query part, C{args} will be C{{'foo': ['bar', 'baz'], "
        "'quux': ['spam']}}.")

    received_headers = Attribute(
        "Backwards-compatibility access to C{requestHeaders}.  Use "
        "C{requestHeaders} instead.  C{received_headers} behaves mostly "
        "like a C{dict} and does not provide access to all header values.")

    requestHeaders = Attribute(
        "A L{http_headers.Headers} instance giving all received HTTP request "
        "headers.")

    headers = Attribute(
        "Backwards-compatibility access to C{responseHeaders}.  Use"
        "C{responseHeaders} instead.  C{headers} behaves mostly like a "
        "C{dict} and does not provide access to all header values nor "
        "does it allow multiple values for one header to be set.")

    responseHeaders = Attribute(
        "A L{http_headers.Headers} instance holding all HTTP response "
        "headers to be sent.")

    def getHeader(key):
        """
        Get an HTTP request header.

        @type key: C{str}
        @param key: The name of the header to get the value of.

        @rtype: C{str} or C{NoneType}
        @return: The value of the specified header, or C{None} if that header
            was not present in the request.
        """


    def getCookie(key):
        """
        Get a cookie that was sent from the network.
        """


    def getAllHeaders():
        """
        Return dictionary mapping the names of all received headers to the last
        value received for each.

        Since this method does not return all header information,
        C{requestHeaders.getAllRawHeaders()} may be preferred.
        """


    def getRequestHostname():
        """
        Get the hostname that the user passed in to the request.

        This will either use the Host: header (if it is available) or the
        host we are listening on if the header is unavailable.

        @returns: the requested hostname
        @rtype: C{str}
        """


    def getHost():
        """
        Get my originally requesting transport's host.

        @return: An L{IAddress}.
        """


    def getClientIP():
        """
        Return the IP address of the client who submitted this request.

        @returns: the client IP address or C{None} if the request was submitted
            over a transport where IP addresses do not make sense.
        @rtype: C{str} or L{NoneType}
        """


    def getClient():
        """
        Return the hostname of the IP address of the client who submitted this
        request, if possible.

        This method is B{deprecated}.  See L{getClientIP} instead.

        @rtype: L{NoneType} or L{str}
        @return: The canonical hostname of the client, as determined by
            performing a name lookup on the IP address of the client.
        """


    def getUser():
        """
        Return the HTTP user sent with this request, if any.

        If no user was supplied, return the empty string.

        @returns: the HTTP user, if any
        @rtype: C{str}
        """


    def getPassword():
        """
        Return the HTTP password sent with this request, if any.

        If no password was supplied, return the empty string.

        @returns: the HTTP password, if any
        @rtype: C{str}
        """


    def isSecure():
        """
        Return True if this request is using a secure transport.

        Normally this method returns True if this request's HTTPChannel
        instance is using a transport that implements ISSLTransport.

        This will also return True if setHost() has been called
        with ssl=True.

        @returns: True if this request is secure
        @rtype: C{bool}
        """


    def getSession(sessionInterface=None):
        """
        Look up the session associated with this request or create a new one if
        there is not one.

        @return: The L{Session} instance identified by the session cookie in
            the request, or the C{sessionInterface} component of that session
            if C{sessionInterface} is specified.
        """


    def URLPath():
        """
        @return: A L{URLPath} instance which identifies the URL for which this
            request is.
        """


    def prePathURL():
        """
        @return: At any time during resource traversal, a L{str} giving an
            absolute URL to the most nested resource which has yet been
            reached.
        """


    def rememberRootURL():
        """
        Remember the currently-processed part of the URL for later
        recalling.
        """


    def getRootURL():
        """
        Get a previously-remembered URL.
        """


    # Methods for outgoing response
    def finish():
        """
        Indicate that the response to this request is complete.
        """


    def write(data):
        """
        Write some data to the body of the response to this request.  Response
        headers are written the first time this method is called, after which
        new response headers may not be added.
        """


    def addCookie(k, v, expires=None, domain=None, path=None, max_age=None, comment=None, secure=None):
        """
        Set an outgoing HTTP cookie.

        In general, you should consider using sessions instead of cookies, see
        L{cyclone.tw.server.Request.getSession} and the
        L{cyclone.tw.server.Session} class for details.
        """


    def setResponseCode(code, message=None):
        """
        Set the HTTP response code.
        """


    def setHeader(k, v):
        """
        Set an HTTP response header.  Overrides any previously set values for
        this header.

        @type name: C{str}
        @param name: The name of the header for which to set the value.

        @type value: C{str}
        @param value: The value to set for the named header.
        """


    def redirect(url):
        """
        Utility function that does a redirect.

        The request should have finish() called after this.
        """


    def setLastModified(when):
        """
        Set the C{Last-Modified} time for the response to this request.

        If I am called more than once, I ignore attempts to set Last-Modified
        earlier, only replacing the Last-Modified time if it is to a later
        value.

        If I am a conditional request, I may modify my response code to
        L{NOT_MODIFIED} if appropriate for the time given.

        @param when: The last time the resource being returned was modified, in
            seconds since the epoch.
        @type when: C{int}, C{long} or C{float}

        @return: If I am a C{If-Modified-Since} conditional request and the
            time given is not newer than the condition, I return
            L{http.CACHED<CACHED>} to indicate that you should write no body.
            Otherwise, I return a false value.
        """


    def setETag(etag):
        """
        Set an C{entity tag} for the outgoing response.

        That's "entity tag" as in the HTTP/1.1 C{ETag} header, "used for
        comparing two or more entities from the same requested resource."

        If I am a conditional request, I may modify my response code to
        L{NOT_MODIFIED} or L{PRECONDITION_FAILED}, if appropriate for the tag
        given.

        @param etag: The entity tag for the resource being returned.
        @type etag: C{str}
        @return: If I am a C{If-None-Match} conditional request and the tag
            matches one in the request, I return L{http.CACHED<CACHED>} to
            indicate that you should write no body.  Otherwise, I return a
            false value.
        """


    def setHost(host, port, ssl=0):
        """
        Change the host and port the request thinks it's using.

        This method is useful for working with reverse HTTP proxies (e.g.  both
        Squid and Apache's mod_proxy can do this), when the address the HTTP
        client is using is different than the one we're listening on.

        For example, Apache may be listening on https://www.example.com, and
        then forwarding requests to http://localhost:8080, but we don't want
        HTML produced by Twisted to say 'http://localhost:8080', they should
        say 'https://www.example.com', so we do::

           request.setHost('www.example.com', 443, ssl=1)
        """



class ICredentialFactory(Interface):
    """
    A credential factory defines a way to generate a particular kind of
    authentication challenge and a way to interpret the responses to these
    challenges.  It creates L{ICredentials} providers from responses.  These
    objects will be used with L{twisted.cred} to authenticate an authorize
    requests.
    """
    scheme = Attribute(
        "A C{str} giving the name of the authentication scheme with which "
        "this factory is associated.  For example, C{'basic'} or C{'digest'}.")


    def getChallenge(request):
        """
        Generate a new challenge to be sent to a client.

        @type peer: L{cyclone.tw.http.Request}
        @param peer: The request the response to which this challenge will be
            included.

        @rtype: C{dict}
        @return: A mapping from C{str} challenge fields to associated C{str}
            values.
        """


    def decode(response, request):
        """
        Create a credentials object from the given response.

        @type response: C{str}
        @param response: scheme specific response string

        @type request: L{cyclone.tw.http.Request}
        @param request: The request being processed (from which the response
            was taken).

        @raise twisted.cred.error.LoginFailed: If the response is invalid.

        @rtype: L{twisted.cred.credentials.ICredentials} provider
        @return: The credentials represented by the given response.
        """



class IBodyProducer(IPushProducer):
    """
    Objects which provide L{IBodyProducer} write bytes to an object which
    provides L{IConsumer} by calling its C{write} method repeatedly.

    L{IBodyProducer} providers may start producing as soon as they have
    an L{IConsumer} provider.  That is, they should not wait for a
    C{resumeProducing} call to begin writing data.

    L{IConsumer.unregisterProducer} must not be called.  Instead, the
    L{Deferred} returned from C{startProducing} must be fired when all bytes
    have been written.

    L{IConsumer.write} may synchronously invoke any of C{pauseProducing},
    C{resumeProducing}, or C{stopProducing}.  These methods must be implemented
    with this in mind.

    @since: 9.0
    """

    # Despite the restrictions above and the additional requirements of
    # stopProducing documented below, this interface still needs to be an
    # IPushProducer subclass.  Providers of it will be passed to IConsumer
    # providers which only know about IPushProducer and IPullProducer, not
    # about this interface.  This interface needs to remain close enough to one
    # of those interfaces for consumers to work with it.

    length = Attribute(
        """
        C{length} is a C{int} indicating how many bytes in total this
        L{IBodyProducer} will write to the consumer or L{UNKNOWN_LENGTH}
        if this is not known in advance.
        """)

    def startProducing(consumer):
        """
        Start producing to the given L{IConsumer} provider.

        @return: A L{Deferred} which fires with C{None} when all bytes have
            been produced or with a L{Failure} if there is any problem before
            all bytes have been produced.
        """


    def stopProducing():
        """
        In addition to the standard behavior of L{IProducer.stopProducing}
        (stop producing data), make sure the L{Deferred} returned by
        C{startProducing} is never fired.
        """

UNKNOWN_LENGTH = u"cyclone.tw.iweb.UNKNOWN_LENGTH"

__all__ = [
#   "IUsernameDigestHash", "ICredentialFactory", "IRequest",
    "ICredentialFactory", "IRequest",
    "IBodyProducer",

    "UNKNOWN_LENGTH"]
