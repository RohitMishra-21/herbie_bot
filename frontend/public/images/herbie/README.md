# H.E.R.B.I.E. Image Assets

Please place your H.E.R.B.I.E. (Fantastic Four robot) images in the appropriate folders:

## Folder Structure:

### `/avatars/`
- `herbie-main-avatar.png` - Main HERBIE robot portrait/face
- `herbie-happy.png` - Happy/friendly expression
- `herbie-thinking.png` - Thoughtful expression
- `herbie-alert.png` - Alert/urgent expression

### `/comics/`
- `herbie-fantastic-four-1.jpg` - HERBIE in action with Fantastic Four
- `herbie-fantastic-four-2.jpg` - HERBIE comic panels
- `herbie-baxter-building.jpg` - HERBIE in the Baxter Building

### `/backgrounds/`
- `fantastic-four-bg.jpg` - Fantastic Four themed background
- `baxter-building-interior.jpg` - Baxter Building interior
- `space-cosmic.jpg` - Space/cosmic background for HERBIE

### `/icons/`
- `herbie-icon-16.png` - Small icon (16x16)
- `herbie-icon-32.png` - Medium icon (32x32)
- `herbie-icon-64.png` - Large icon (64x64)

## Recommended Image Specs:

- **Avatars**: 200x200px or higher, PNG with transparency
- **Comics**: Any resolution, JPG or PNG
- **Backgrounds**: 1920x1080px or higher, JPG
- **Icons**: Exact pixel dimensions, PNG with transparency

## Usage in Code:

Images will be accessible via:
```javascript
// Avatar
<img src="/images/herbie/avatars/herbie-main-avatar.png" alt="HERBIE" />

// Background
background-image: url('/images/herbie/backgrounds/fantastic-four-bg.jpg');

// Icons
<img src="/images/herbie/icons/herbie-icon-32.png" alt="HERBIE Icon" />
```

Once you add the images, they'll automatically appear in the interface!