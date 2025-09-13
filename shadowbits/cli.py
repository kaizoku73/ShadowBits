import argparse
from .emb_img import embed_file  
from .ext_img import extract_file
from .emb_aud import embed_audio
from .ext_aud import extract_audio


def main():
    parser = argparse.ArgumentParser(description='Steganography tool for hiding files in images')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')


    # Embed command for image
    img_parser = subparsers.add_parser('img', help='Image operations')
    img_subparser = img_parser.add_subparsers(dest='action' , help='Image actions')
    embed_cmd = img_subparser.add_parser('embed', help='Hide a file in an image')
    embed_cmd.add_argument('--in', dest='input', required=True, help='File to hide')    
    embed_cmd.add_argument('--cover', dest='image', required=True, help='Cover image')
    embed_cmd.add_argument('--key', required=True, help='Secret key for randomization')

    # Extract command for image
    extract_cmd = img_subparser.add_parser('extract', help='Extract hidden file from image')
    extract_cmd.add_argument('--stego', required=True, help='Image with hidden file')
    extract_cmd.add_argument('--key', required=True, help='Secret key used for hiding')

    # Embed command for audio
    aud_parser = subparsers.add_parser('aud', help='Audio operation')
    aud_subparser = aud_parser.add_subparsers(dest='action', help='Audio actions')
    embed_audio_cmd = aud_subparser.add_parser('embed', help='Hide a file in an audio file')
    embed_audio_cmd.add_argument('--in', dest='input', required=True, help='File to hide')
    embed_audio_cmd.add_argument('--cover', dest='song', required=True, help='Cover audio')
    embed_audio_cmd.add_argument('--key', required=True, help='Secret key to randomize bits')

    # Extract command for audio
    extract_audio_cmd = aud_subparser.add_parser('extract', help='Extract hidden file from audio')
    extract_audio_cmd.add_argument('--stego', required=True, help='Audio with hidden file')
    extract_audio_cmd.add_argument('--key', required=True, help='Secret key used for hiding')


    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        exit(1)

    try:
        if args.command == 'img':
            if args.action == 'embed':
                embed_file(args.image, args.input, args.key)
                print(f"Successfully embedded {args.input} in {args.image}.")
            elif args.action == 'extract':
                extract_file(args.stego, args.key)
                print(f"Successfully extracted hidden file from {args.stego}.")
            else:
                img_parser.print_help()
                raise SystemExit(1)
        
        elif args.command == 'aud':
            if args.action == 'embed':
                embed_audio(args.song, args.input, args.key)
                print(f"Successfully embedded {args.input} in {args.song}.")
            elif args.action == 'extract':
                extract_audio(args.stego, args.key)
                print(f"Successfully extracted hidden file from {args.stego}.")
            else:
                aud_parser.print_help()
                raise SystemExit(1)

    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == '__main__':
    main()