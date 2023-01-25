# Custom views

Instruction on how to use custom views.

## views.py file

Firstly a `views.py` file must be created - it can be based or copied from `example.py` file. It must contain a list `VIEWS` containing *View* class objects only.

## View class

Every custom view must be a child of a `View` class. Also a method `_epd_change` must be defined with `first_call` argument - this methods interacts with EPD. This parameter might be useful to determine if a current view was displayed during current interval.

### Arguments passed to a constructor

In addition each view instance must be initiated with a name and interval. Optional third parameter is an angle.

| Parameter | Purpose | Value type |
| --- | --- | --- |
| name | View name | string |
| interval | Interval by which a method show will be called in a loop. To disable this feature set it to 0 | integer |
| view_angle `[Optional]` | Angle by which a final view will be rotated. By default it uses `view_angle` from config. Rotating is triggered via `_rotate_image()` method of View | integer |

### View fallback

In addition a **fallback** can be displayed if a `_epd_change` method will fail with an exception. To achieve this:

- `_epd_change` method bust be decorated with `@view_fallback` decorator (imported from `helpers.py`) and
- `_fallback` method which displays fallback view must be defined.

### Conditional showing

By default if a view has interval it triggers EPD change within each loop - even when the data itself didn't changed and this operation is redundant. As an example - a basic clock view (HH:MM) which should check for current time in each second (interval = 1) but update only once per minute. To achieve this a method `_conditional` must be overrided and return boolean value based on desired condition.

### Examplary usage of custom Views

Basing on `example.py` and using defined DummyView, ConditionalDummyView and BrokenDummyView class a `VIEWS` list might look like:

    VIEWS = [
        DummyView('Dummy view 1', 0),
        DummyView('Dummy view 2', 6, 180),
        DummyView('Dummy view 3', 0),
        ConditionalDummyView('Conditional view 4', 7),
        BrokenDummyView('Broken dummy view 5', 0)
    ]

and:

- views 1 and 3 have no `interval` (0)
- views 2 and 4 have interval (in seconds) by which a `show` method will be called unless a switching view action gets called.
- view 2 is rotated by 180 degrees
- view 4 will trigger EPD change conditionally (since `_conditional` method is overrided)
- view 5 will show a fallback image since its `show` method raises an exception (but is decorated with a `@view_fallback`)

## Custom requirements

If a View uses any additional Python packages they should be added to a `controller/custom_views/custom_requirements.txt` file. If this file doesn't exist it must be created first.
