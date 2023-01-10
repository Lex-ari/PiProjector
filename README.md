# PiProjector
## An Architect's / Engineer's / Mathematician's / Scientist's favorite tool for cutting pies.

This project projects a laser that shows the user where to cut on a pie / cake at exact fractions. No more arguing about who's cut is bigger!

I already own a Logitech C920 webcam and had some money to spend from Christmas. I ultimately decided that getting a projector would be a fun purchase. For this project, the projector should not be too expensive, yet still be able to project at demands. The projector chosen has a native resolution of 720p and supports USB power and HDMI input, making it extremely portable.

Tools like this currently exist in the app store. However, these tools simply project a transparent image on top of a phone's camera output, meaning that the user would have to cut their pie / cake looking through the phone. This project uses lasers, which aided with a stand, can freely cut their dessert with both hands (and lasers are much cooler).

Current Equipment:

- Logitech C920 Pro Webcam
- YG300 Pro Projector found here: https://www.amazon.com/Projector-Meer-Compatible-Firestick-Controller/dp/B09XD641MV/ref=sr_1_3?crid=1HRXJGCM9XQ1H&keywords=YG300+pro&qid=1673328878&sprefix=yg300+pro%2Caps%2C131&sr=8-3&ufe=app_do%3Aamzn1.fos.006c50ae-5d4c-4777-9bc0-4513d670b6bc
- Acer Aspire R5-471TG.

**Features:**
- [CURRENT PROGRESS] Automatic Camera / Projection Calibration
  - Takes multiple images, uses image subtraction, and template matching to solve for center, skewness, and area of projection.
- [CURRENT PROGRESS] Projection / Camera CAD mount
- [PLANNED] Optical Flow tracking of pie
- [PLANNED] Circle fraction projections
  - [FUTURE] Multiple fraction support
- [PLANNED] Magnification Lens for Projector for close-up projection

![image](https://user-images.githubusercontent.com/65744075/211457048-6a421419-286a-4573-a0d7-261faccb217f.png)
