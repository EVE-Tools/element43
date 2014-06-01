/**
 * jQuery ticker plugin
 *
 * By Andrew Betts <andrew.betts@assanka.net>
 *
 * Copyright (c) 2010 Assanka Limited
 *
 * -----------
 *
 * Licenced under the terms of the MIT licence, reproduced below:
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 *
 * -----------
 *
 * A ticker tape animation plugin, designed to emulate continuous tickers of the
 * type typically seen on 24 hour news channels. Requires native CSS3
 * transitions which are currently only available in webkit based browsers.
 *
 * Features:
 *
 * + When the ticker reaches the end of the text, the text
 *   at the beginning of the ticker follows on immediately,
 *   creating a continuous loop
 *
 * + Changes to the contents of the ticker are reflected
 *   seamlessly - content is never added or removed in the
 *   visible portion of the ticker
 *
 * @author     Andrew Betts <andrew.betts@assanka.net>
 * @copyright  Assanka Limited
 * @licence    http://www.opensource.org/licenses/mit-license.php
 */
(function($) {

    $.fn.ticker = function(options) {
        settings = jQuery.extend({
            pxpersec: 30
        }, options);
        if (this.length != 1) throw "Ticker can only be attached to a single element";
        if (this.children('ul').length != 1) throw "Ticker container must contain a UL, eg <div id='ticker'><ul></ul></div>";
        return new $.ticker(this, settings);
    };

    $.ticker = function(el, settings) {

        var addqueue = [];
        var removequeue = [];
        var numsegs;
        var updatecount = 0;
        var thisticker = this;
        var msgwidth = 0;
        var isscrolling = 0;

        var elcont = el;
        var eltape = el.children().first();
        eltape.css({
            "margin": 0,
            "padding": 0,
            "listStyleType": 'none',
            "whiteSpace": 'nowrap',
            'float': 'left',
            "position": 'absolute',
            "right": 0,
            "oTransition": 'right 0s linear 0',
            "webkitTransition": 'right 0s linear 0',
            "mozTransition": 'right 0s linear 0ms',
            "transition": 'right 0s linear 0ms'
        });
        elcont.css({
            overflow: 'hidden'
        });
        if (!elcont.css('float') || elcont.css('float') == 'none') elcont.css('display', 'block');

        if (eltape.children('li').length) initTape();


        /* Private methods */

        function initTape() {

            numsegs = 1;

            // Mark each message in the list
            if (!eltape.children('li').length) throw "Cannot initialise ticker: Nothing in it";
            eltape.children('li').each(function() {
                if (!$(this).attr('id')) $(this).attr('id', 'msg' + Math.ceil(Math.random() * 99999999));
                $(this).addClass('seg1').attr('seg', 1);
            });

            // Apply transiton CSS to the tape
            isscrolling = 1;
            updatecount = 1;
            eltape.bind('webkitTransitionEnd', slide);
            eltape.bind('oTransitionEnd', slide);
            eltape.bind('mozTransitionEnd', slide);
            eltape.bind('transitionEnd', slide);
            slide();
        }

        function slide(e) {

            // Copy each segment over the one preceding it
            if (updatecount) {
                if (numsegs > 1) {
                    for (var i = (numsegs - 1); i >= 1; i--) {
                        eltape.find('.seg' + (i + 1)).remove();
                        eltape.find('.seg' + i).clone().removeClass('seg' + i).removeAttr('id').addClass('seg' + (i + 1)).attr('seg', (i + 1)).insertBefore(eltape.find('.seg' + i).first());
                    }
                }

                // If the ticker is now empty, delete all shadow segments and stop
                if (eltape.find('.empty').length) {
                    eltape.unbind().css({
                        transitionDuration: '0s'
                    }).children().remove();
                    isscrolling = 0;
                    return;
                }

                // Add or remove segments as necessary
                var widths = calcWidths();
                if (widths.total < (elcont.width() + widths.seg1)) {
                    var content = eltape.children('.seg' + numsegs);
                    content = content.clone().removeAttr('id').removeClass('seg' + numsegs);
                    if (!widths['seg' + numsegs]) throw "Ticker is zero-width";
                    var numrequired = Math.ceil((elcont.width() + widths.seg1 - widths.total) / widths['seg' + numsegs]);
                    for (var i = 1; i <= numrequired; i++) {
                        numsegs++;
                        eltape.prepend(content.clone().addClass('seg' + numsegs).attr('seg', numsegs));
                        widths['seg' + numsegs] = widths['seg' + (numsegs - 1)];
                        widths.total += widths['seg' + numsegs];
                    }
                }
                if (widths.total > (elcont.width() + (widths.seg1 * 2))) {
                    eltape.find('.seg' + numsegs).remove();
                    numsegs--;
                    widths.total -= widths['seg' + (numsegs + 1)];
                    delete widths['seg' + (numsegs + 1)];
                }

                msgwidth = widths.seg1;
                eltape.width(widths.total);
                updatecount--;
            }

            // Modify the last segment to add/remove queued elements
            if (removequeue.length || addqueue.length) {
                if (removequeue.length) {
                    for (var i = removequeue.length - 1; i >= 0; i--) $(removequeue[i]).remove();
                    removequeue = [];

                    // If master segment is now zero-width, add a .empty message that is the width of the parent container
                    if (!eltape.find('.seg1').length) $('<li class="seg1 empty"></li>').width(elcont.width()).appendTo(eltape);
                }
                if (addqueue.length) {
                    for (var i = addqueue.length - 1; i >= 0; i--) {
                        $(addqueue[i]).addClass('seg1').attr('seg', 1).appendTo(eltape);
                    }
                    addqueue = [];

                    // Remove any .empty messages
                    eltape.find('.seg1').filter('.empty').remove();
                }

                // Recalculate widths
                var widths = calcWidths();
                msgwidth = widths.seg1;
                eltape.width(widths.total);

                // Start cascade
                updatecount = numsegs;
            }

            // Reposition the tape to move the last segment just off the right side of the screen
            eltape.css({
                "webkitTransitionDuration": '0s',
                "mozTransitionDuration": '0s',
                "oTransitionDuration": '0s',
                "transitionDuration": '0s'
            });
            eltape.css({
                "right": '-' + msgwidth + 'px'
            });

            // Calculate duration of animation to achieve desired speed, resume scrolling
            dur = Math.floor(msgwidth / settings.pxpersec);
            setTimeout(function() {
                eltape.css({
                    "webkitTransitionDuration": dur + 's',
                    "mozTransitionDuration": dur + 's',
                    "oTransitionDuration": dur + 's',
                    "transitionDuration": dur + 's'
                });
                eltape.css({
                    right: 0 + 'px'
                });
            }, 0);
        }


        /* Private methods */

        function calcWidths() {
            var widths = {
                total: 0
            };
            eltape.children().each(function() {
                if (typeof widths['seg' + $(this).attr('seg')] == 'undefined') widths['seg' + $(this).attr('seg')] = 0;
                widths['seg' + $(this).attr('seg')] += $(this).outerWidth();
                widths.total += $(this).outerWidth();
            });
            return widths;
        }


        /* Public methods */

        // Add a new item to the ticker.  Pass a reference to an LI that is to be added to the ticker
        this.addMsg = function(el) {
            if (typeof el == 'string') el = $('<li>' + el + '</li>');
            if (!el.attr('id')) el.attr('id', 'msg' + Math.ceil(Math.random() * 99999999));
            if (isscrolling) {
                addqueue.push(el);
            } else {
                eltape.append(el);
            }
            return el.attr('id');
        };

        // Remove an item from the ticker.  Pass a reference to an LI in segment 1.
        this.removeMsg = function(el) {
            if (typeof el == 'string') el = $('#' + el);
            removequeue.push(el);
        };

        // Start if not already running
        this.start = function() {
            if (!isscrolling) initTape();
        };

        // Report current status of ticker
        this.isScrolling = function() {
            return (isscrolling === true);
        };
    };
})(jQuery);