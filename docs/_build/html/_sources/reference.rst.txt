Reference
=========

Osbject
^^^^^^^

.. py:class:: Osbject

    .. py:method:: __init__(path, layer, origin, posx, posy, frame_count=None, frame_rate=None, loop=None)

        Creates an instance of Osbject.
        
        :param str path: Path to an image file, relative to the result file
        :param str layer: Layer in the storyboard (Background, Fail, Pass, Foreground)
        :param str origin: Origin of the image (TopLeft, TopCentre, TopRight, CentreLeft, Centre, CentreRight, BottomLeft, BottomCentre, BottomRight)
        :param int posx: Implicit position on X axis
        :param int posy: Implicit position on Y axis
        :param frame_count: Number of frames, if using animation
        :type frame_count: int or None
        :param frame_rate: Frames per second, if using animation
        :type frame_rate: int or None
        :param loop: Type of loop, if using animation (LoopForever, LoopOnce)
        :type loop: str or None

    .. py:method:: add(args)

        Joins a tuple and adds to list of storyboarding commands. Only for developers.

        :param tuple args: Tuple of strings to join

    .. py:method:: fade(easing, start, end, start_fade, end_fade, loop=False)

        Changes the transparency of an object.

        :param int easing: Type of easing to use (1 - 34)
        :param int start: Time to start (ms) the fade
        :param int end: Time to end (ms) the fade
        :param float start_fade: Value of fade at the start (0 = invisible, 1 = fully visible)
        :param float end_fade: Value of fade at the end (0 = invisible, 1 = fully visible)
        :param loop: If is a part of the loop command
        :type loop: bool or None

    .. py:method:: move(easing, start, end, start_movex, start_movey, end_movex, end_movey, loop=False)

        Moves an object on X and Y axis.

        :param int easing: Type of easing to use (1 - 34)
        :param int start: Time to start (ms) the move
        :param int end: Time to end (ms) the move
        :param int start_movex: Position on X axis at the start
        :param int start_movey: Position on Y axis at the start
        :param int end_movex: Position on X axis at the end
        :param int end_movey: Position on Y axis at the end
        :param loop: If is a part of the loop command
        :type loop: bool or None

    .. py:method:: movex(easing, start, end, start_movex, end_movex, loop=False, swap=False)

        Moves an object on X axis.

        :param int easing: Type of easing to use (1 - 34)
        :param int start: Time to start (ms) the move
        :param int end: Time to end (ms) the move
        :param int start_movex: Position on X axis at the start
        :param int end_movex: Position on X axis at the end
        :param loop: If is a part of the loop command
        :type loop: bool or None
        :param swap: Change axis to Y (use movey method instead)
        :type loop: bool or None

    .. py:method:: movey(easing, start, end, start_movey, end_movey, loop=False)

        Moves an object on Y axis.

        :param int easing: Type of easing to use (1 - 34)
        :param int start: Time to start (ms) the move
        :param int end: Time to end (ms) the move
        :param int start_movey: Position on Y axis at the start
        :param int end_movey: Position on Y axis at the end
        :param loop: If is a part of the loop command
        :type loop: bool or None

    .. py:method:: scale(easing, start, end, start_scale, end_scale, loop=False)

        Scales an object up or down.

        :param int easing: Type of easing to use (1 - 34)
        :param int start: Time to start (ms) the scale
        :param int end: Time to end (ms) the scale
        :param float start_scale: Value of scale at the start
        :param float end_scale: Value of scale at the end
        :param loop: If is a part of the loop command
        :type loop: bool or None

    .. py:method:: vecscale(easing, start, end, start_scalex, start_scaley, end_scalex, end_scaley, loop=False)

        Scale an object disproportionately on X and Y axis.

        :param int easing: Type of easing to use (1 - 34)
        :param int start: Time to start (ms) the vector scale
        :param int end: Time to end (ms) the vector scale
        :param float start_scalex: Value of scale at the start on X axis
        :param float start_scaley: Value of scale at the start on Y axis
        :param float end_scalex: Value of scale at the end on X axis
        :param float end_scaley: Value of scale at the end on Y axis
        :param loop: If is a part of the loop command
        :type loop: bool or None

    .. py:method:: rotate(easing, start, end, start_rotate, end_rotate, loop=False)

        Rotates an object.

        :param int easing: Type of easing to use (1 - 34)
        :param int start: Time to start (ms) the rotation
        :param int end: Time to end (ms) the rotation
        :param float start_rotate: Value of rotation at the start
        :param float end_rotate: Value of rotation at the end
        :param loop: If is a part of the loop command
        :type loop: bool or None

    .. py:method:: colour(easing, start, end, r, g, b, end_r, end_g, end_b, loop=False)

        Changes a color of an object. May not work as intended with non-grayscale images.

        :param int easing: Type of easing to use (1 - 34)
        :param int start: Time to start (ms) the colour change
        :param int end: Time to end (ms) the colour change
        :param int r: Value of red colour (0 - 255) at the start
        :param int g: Value of green colour (0 - 255) at the start
        :param int b: Value of blue colour (0 - 255) at the start
        :param int end_r: Value of red colour (0 - 255) at the end
        :param int end_g: Value of green colour (0 - 255) at the end
        :param int end_b: Value of blue colour (0 - 255) at the end
        :param loop: If is a part of the loop command
        :type loop: bool or None

    .. py:method:: para(easing, start, end, parameter)

        Applies storyboarding parameter to an object.

        :param int easing: Type of easing to use (1 - 34)
        :param int start: Time to start (ms) the parameter
        :param int end: Time to end (ms) the fade
        :param str parameter: Storyboarding parameter (H, V, A)

    .. py:method:: loop(start, loop_count)

        Creates a loop of storyboarding commands. To utilize this, affected methods must set loop to True.

        :param int start: Time to start (ms) the loop
        :param int loop_count: Times to repeat the loop.

    .. py:method:: trigger(trigger, start, loop_count)

        Creates a trigger to run commands on a specific action.

        :param str trigger: Type of trigger (Failing, Passing, or HitSound[...])
        :param int start: Time to start (ms) the fade
        :param int loop_count: Times to repeat the loop.

    .. py:staticmethod:: minimize(variable, force=False)

        Creates a variable for a string.

        :param str variable: String to minimize
        :param force: If minimization should be forced
        :type force: bool or None

    .. py:classmethod:: end(osb_file)

        Creates an output .osb file.

        :param str osb_file: Path to the output file

    .. py:classmethod:: end_minimize(osb_file)

        Creates an output .osb file, utilizes minimization.

        :param str osb_file: Path to the output file

    .. py:classmethod:: set_minimize_threshold(threshold)

        Sets a threshold for minimization.

        :param int threshold: Maximum length of a string to minimize

    .. py:classmethod:: set_minimize_time(value)

        Sets whether time values should be minimized.

        :param bool value: If time should be minimized

    .. py:classmethod:: minimize_force(variable)

        Creates a variable for a string regardless of threshold.

        :param str variable: String to minimize

Additional functions
^^^^^^^^^^^^^^^^^^^^

.. py:function:: sine(har, radius, height)

    Creates a list of sine Y values. For usage in spectrum or sine-like patterns.

    :param int har: Number of samples
    :param float radius: Multiplication of the sine
    :param int height: Height of the sine
    :return: List of sine Y values
    :rtype: list

.. py:function:: generate_circle(r, n)

    Generates values to create a circle. Used by circle.

    :param list r: Radius
    :param list n: Number of samples
    :return: X and Y values of the circle
    :rtype: (float, float)

.. py:function:: circle(har, radius)
    
    Creates a circle.
    
    :param float har: Number of samples
    :param int r: Radius
    :return: X and Y positions of the circle
    :rtype: (dict, dict)

.. py:function:: variable_name()

    Creates a variable name for minimization in the storyboard file.

    :return: Variable name
    :rtype: str

.. py:function:: check_path(path)

    Checks if path is valid.

    :param str path: Path to check
    :return: True if is valid
    :rtype: bool

.. py:function:: check_layer(layer)

    Checks if layer is valid.

    :param str layer: Layer to check
    :return: True if is valid
    :rtype: bool

.. py:function:: check_origin(origin)

    Checks if origin is valid.

    :param str origin: Origin to check
    :return: True if is valid
    :rtype: bool

.. py:function:: check_int(integer)

    Checks if value is integer.

    :param int integer: Value to check
    :return: True if is valid
    :rtype: bool

.. py:function:: check_easing(easing)

    Checks if easing is valid.

    :param int easing: Easing to check
    :return: True if is valid
    :rtype: bool

.. py:function:: check_loop(loop)

    Checks if loop is valid.

    :param str loop: Loop to check
    :return: True if is valid
    :rtype: bool

.. py:function:: check_dec(dec)

    Checks if value is decimal.
    
    :param float dec: Value to check
    :return: True if is valid
    :rtype: bool

.. py:function:: check_time(start, end)

    Checks if time is valid.

    :param int start: Start time to check
    :param int end: End time to check
    :return: True if is valid
    :rtype: bool

.. py:function:: check_colours(args)

    Checks if colors are valid.

    :param tuple args: Colors to check.
    :return: True if is valid
    :rtype: bool

.. py:function:: check_trigger(trigger)

    Checks if trigger is valid.

    :param str trigger: Trigger to check
    :return: True if is valid
    :rtype: bool

.. py:function:: spectrum(wav_file, bar_file, mi, mx, har, start, end, posx, posy, layer, origin, gap=0, arrange="", radius=30, sine_height=6.1)

    Creates a spectrum from a wave file.

    :param str wav_file: Path to wave (.wav) file (Use a file without metadata in case of issues)
    :param str bar_file: Path to an image file, relative to the result file
    :param float mi: Minimum height of the spectrum
    :param float mx: Maximum height of the spectrum
    :param int har: Number of samples
    :param int start: Start time of the spectrum
    :param int end: End time of the spectrum
    :param int posx: Position of the spectrum on X axis
    :param int posy: Position of the spectrum on Y axis
    :param str layer: Layer in the storyboard (Background, Fail, Pass, Foreground)
    :param str origin: Origin of the image (TopLeft, TopCentre, TopRight, CentreLeft, Centre, CentreRight, BottomLeft, BottomCentre, BottomRight)
    :param int gap: Gap between each bar
    :param string arrange: How to arrange the spectrum (circle, sine) or empty for line
    :param float radius: Radius of the sine
    :param float sine_height: Height of the sine
    :return: List of Osbjects
    :rtype: list
