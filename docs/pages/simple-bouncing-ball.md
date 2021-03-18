---
layout: content-page
title: Simple Bouncing Ball
---

# Simple Bouncing Ball
### Tox - container_simple_bouncing_ball

**Original post / question**

>Hello,

>I've been wanting to do some simple custom physics for a while, but have not been able to do so yet. I keep coming back to the Nature of Code -book by Dan Shiffman.

>Would it make any sense trying to port this: [http://natureofcode.com/book/chapter-1-vectors/] to this: [https://www.derivative.ca/wiki088/index.php?title=Vector_Class]

>Python is slow right? Trying to do that with networks of CHOPS is probably slower. Importing javascript would probably be a quick process(if it's possible??), but whatever style, i'd need it to perform with a decent fps too.

>Any tips for a simulation newb?

CHOPs would be a fast way to do this since they're essentially just C++ with some exposed parameters.

CHOP math, generally speaking, is very fast - for the vast majority of movement operations it's an excellent place to start, unless you're wanting to calculate the vectors of millions of particles. When you start to look at doing particle simulations, then GLSL is the place to look. If you look in the pallet you can find a GL particle example to pull apart.

Here's a start with the most rudimentary approach that Shiffman describes - where direction changes when a location value exceeds the bounds of the texture.

This example is all CHOP math and exports - you'll also notice that the circle itself isn't doing the transform operations, but rather another Transform TOP. This is slightly faster as the circle TOP is responsible for rendering the circle and it's transformation. This difference is largely inconsequential, but is slightly faster at the cost of using a little more VRAM.

---
#### Created 09.10.2016
*Matthew Ragan*