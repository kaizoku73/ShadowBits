import argparse
from emb_img import embed_file  
from ext_img import extract_file
from emb_aud import embed_audio
from ext_aud import extract_audio


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Steganography tool for hiding files in images')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')


    # Embed command for image
    embed_cmd = subparsers.add_parser('img-embed', help='Hide a file in an image')
    embed_cmd.add_argument('--in', dest='input', required=True, help='File to hide')    
    embed_cmd.add_argument('--cover', dest='image', required=True, help='Cover image')
    embed_cmd.add_argument('--key', required=True, help='Secret key for randomization')

    # Extract command for image
    extract_cmd = subparsers.add_parser('img-extract', help='Extract hidden file from image')
    extract_cmd.add_argument('--stego', required=True, help='Image with hidden file')
    extract_cmd.add_argument('--key', required=True, help='Secret key used for hiding')

    # Embed command for audio
    embed_audio_cmd = subparsers.add_parser('aud-embed', help='Hide a file in an audio file')
    embed_audio_cmd.add_argument('--in', dest='input', required=True, help='File to hide')
    embed_audio_cmd.add_argument('--cover', dest='song', required=True, help='Cover audio')
    embed_audio_cmd.add_argument('--key', required=True, help='Secret key to randomize bits')

    # Extract command for audio
    extract_audio_cmd = subparsers.add_parser('aud-extract', help='Extract hidden file from audio')
    extract_audio_cmd.add_argument('--stego', required=True, help='Audio with hidden file')
    extract_audio_cmd.add_argument('--key', required=True, help='Secret key used for hiding')


    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        exit(1)

    try:
        if args.command == 'img-embed':
            embed_file(args.image, args.input, args.key)
            print(f"Successfully embedded {args.input} in {args.image}.")
        elif args.command == 'img-extract':
            extract_file(args.stego, args.key)
            print(f"Successfully extracted hidden file from {args.stego}.")
        elif args.command == 'aud-embed':
            embed_audio(args.song, args.input, args.key)
            print(f"Successfully embedded {args.input} in {args.song}.")
        elif args.command == 'aud-extract':
            extract_audio(args.stego, args.key)
            print(f"Successfully extracted hidden file from {args.stego}.")

    except Exception as e:
        print(f"Error: {e}")
        exit(1)