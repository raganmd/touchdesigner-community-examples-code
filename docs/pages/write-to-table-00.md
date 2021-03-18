---
layout: content-page
title: Write Values to a Table
---

# Write Vals to a Table
### tox: container_write_button_vals_to_table
_**8.3.16**_

**Original post / question**

>I have a follow up question about replicator comps. I have my UI successfully being built now, but now I want to create a table storing the values from the "out" nodes of each item the replicator comp creates. Can't figure it out.

>a CHOP or DAT execute DAT that's set to target the correct table location will do the trick.

>Thanks! Forgive my ignorance, but how do I target a table location? For eg. There are 10 items currently created by the replicator comp. I want the string value of each items "out" node updated to a table in the row order based on the items number?

In the panel execute we can target the panels of all operators in this part of the network with the * wildcard.

Next we need to figure out how that corresponds to a table.

```python
    def valueChange(panelValue):
       target_row                  = panelValue.owner.digits
       table                       = op( 'table_save' )
       
       table[ target_row, 1 ]      = panelValue

       return
```


Here it's important to realize that [panelValue is actually an object.](
http://www.derivative.ca/wiki088/index.php?title=PanelValue_Class)

That means we can determine the row in the table that corresponds to the digits of the button pressed. You can see we do this with panelValue.owner.digits, once we know the row, we can then target that location with a [ row, column ] address.

Written out the long way might be:

```python
op( 'table_save' )[ 0, 1 ] = 1
```

This script would change the value of a cell to 1. Instead we want to change the value of the table to match the state of the button. I like using variables to make my scripts easier to read later, but we could also write the longer code above like this:

```python
    def valueChange(panelValue):
       op( 'table_save' )[ panelValue.owner.digits, 1 ] = panelValue
       return
```