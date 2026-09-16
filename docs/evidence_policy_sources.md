# Adopted Evidence and Decision Rules

The prototype separates retailer requirements from project-defined AI thresholds.
This avoids presenting experimental confidence scores as official store policy.

## 1. Text and order evidence

Cotton On Australia's damaged-order guidance asks customers to identify the
order and provide details about the damaged product. The prototype maps these
requirements to order ID validation, claim text, product information, and the
refund amount retrieved from the original order.

Source: https://help.cottonon.com/hc/en-us/articles/900002180866-My-order-has-arrived-damaged-or-faulty

## 2. Image and damage evidence

Cotton On asks for a photo of damaged items. ASOS may ask customers to provide a
photo when a faulty item cannot use the standard return path and states that
returned items may be inspected. The prototype maps these requirements to image
quality, image usability, damage detection, damage confidence, claim-image
consistency, and image-order matching.

Sources:

- https://help.cottonon.com/hc/en-us/articles/900002180866-My-order-has-arrived-damaged-or-faulty
- https://www.asos.com/au/customer-care/order-issues/somethings-wrong-with-my-item-what-do-i-do/

## 3. Automatic decision baseline

The automatic-decision thresholds are project-defined. They are not taken from
Cotton On or ASOS. Automatic approval requires a valid order, policy eligibility,
usable visible evidence, detected damage, claim-image consistency of at least
0.50, high evidence confidence of at least 0.80, and LOW refund risk. Other
combinations request more evidence or route the case to human review.

These thresholds are an initial research baseline and must be evaluated on a
larger labelled dataset before any real-world use.

Accessed: 16 September 2026.
